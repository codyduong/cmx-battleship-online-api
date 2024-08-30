import logging
import uuid
from django_utils_morriswa.exceptions import BadRequestException
import datetime

from app import connections
from app.utils import id_generator
from django.db import IntegrityError
from user_session.models import UserSession, GameRequest


def get_valid_id() -> str:
    gen_id = id_generator(size=4)
    available: bool
    with connections.cursor() as db:
        db.execute("select 1 from user_session where player_id = %s", (gen_id,))
        result = db.fetchone()
        available = result is None

    if not available:
        return get_valid_id()
    return gen_id


def start_session(session: UserSession) -> dict:
    try:
        gen_session_id: uuid
        gen_player_id: str
        with connections.cursor() as db:
            gen_session_id = uuid.uuid4()
            gen_player_id = get_valid_id()

            db.execute("""
                insert into user_session (session_id, player_id, player_name, num_ships)
                values (%s, %s, %s, %s)
            """, (gen_session_id, gen_player_id, session.player_name, session.num_ships))

        return {
            'session_id': gen_session_id,
            'player_id': gen_player_id
        }
    except e:
        logging.error('error on start_session', e)


def end_session(session_id: uuid) -> dict:
    try:
        with connections.cursor() as db:
            db.execute("""
                delete from user_session where session_id = %s
            """, (session_id,))
    except e:
        logging.error('error on end_session', e)

def get_game_request(session_id: uuid) -> list[GameRequest]:

    db_result_one: dict
    db_result_two: list[dict]
    with connections.cursor() as db:
        db.execute("select player_id from user_session where session_id = %s", (session_id,))
        db_result_one = db.fetchone()
        player_id = db_result_one.get('player_id')
        if db_result_one is None or player_id is None:
            raise BadRequestException("Player id cannot be found")

        db.execute("""
            select gr.player_invite_from as player_id,
                   us.player_name as player_name,
                   gr.game_request_id as game_request_id
                   from game_request gr 
                   left join user_session us
                   on gr.player_invite_from = us.player_id
                   where gr.player_invite_to = %s 
        """,(player_id,))

        db_result_two: list = db.fetchall()

        return [GameRequest(data) for data in db_result_two]
        
def create_game_request(session_id: uuid, player_id: str):

    with connections.cursor() as db:
        db.execute("SELECT player_id FROM user_session WHERE session_id = %s",
                   (session_id,))
        result = db.fetchone()

        if result is None:
            raise BadRequestException('Invalid session')
            
        current_player_id = result.get('player_id')

        request_create_time = datetime.datetime.now()
        request_expire_time = request_create_time + datetime.timedelta(minutes=10)

        db.execute("INSERT INTO game_request (player_invite_from, player_invite_to, game_request_created, game_request_expiration) VALUES (%s,%s,%s,%s)",
                   (current_player_id, player_id, request_create_time, request_expire_time))

