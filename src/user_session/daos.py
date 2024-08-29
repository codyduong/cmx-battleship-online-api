import logging
import uuid
from django_utils_morriswa.exceptions import BadRequestException

from app import connections
from app.utils import id_generator
from django.db import IntegrityError
from user_session.models import UserSession, GameRequest
from user_session.views import GameRequestView


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

    with connections.cursor() as db:
        db.execute("select player_id from user_session where session_id = %s", (session_id,))
        player_id = db.fetchone()
        if player_id is None: 
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

        request = db.fetchall()
        if request is None:
            return []
        
        return [GameRequest(data) for data in request]
        
