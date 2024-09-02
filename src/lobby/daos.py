import logging
import uuid
from django_utils_morriswa.exceptions import BadRequestException
import datetime

from app import connections
from django.db import IntegrityError
from lobby.models import GameRequest


def get_game_requests(player_id: str) -> list[GameRequest]:

    db_result: list[dict]
    with connections.cursor() as db:
        db.execute("""
            select 
                gr.player_invite_from as player_id,
                us.player_name as player_name,
                gr.game_request_id as game_request_id
            from game_request gr 
            left join user_session us
            on gr.player_invite_from = us.player_id
            where 
                gr.player_invite_to = %s 
                and gr.game_request_created between NOW() - INTERVAL '10 MINUTES' and NOW()
        """,(player_id,))

        db_result: list = db.fetchall()

        return [GameRequest(data) for data in db_result]
        
def create_game_request(current_player_id: str, requested_player_id: str):

    with connections.cursor() as db:
        db.execute("""
            insert into game_request (player_invite_from, player_invite_to) 
            VALUES (%s,%s)
        """, (current_player_id, requested_player_id,))

def accept_match_request(game_request_id: int, current_player_id: str, request_player_id):

    with connections.cursor() as db:
        db.execute("""
            insert into game_session (game_id, player_one_id, player_two_id)
            values (%s,%s,%s)
        """, (game_request_id, current_player_id, request_player_id))

def request_random_match():
    print('TODO')

def game_status(game_id: int):
    with connections.cursor() as db:
        db.execute("""
            select player_two_id, player_two_id, game_expiration, game_phase, game_state
                   FROM game_session
            where game_id = %s
        """), (game_id)

def init_move(state: object):
    try:
        print('hi')
        with connections.cursor() as db:
            db.execute("""select state
                       from game_session
                       where state = $s""", (state))
    except Exception as e:
        logging.error('Unable to process init move', e)



def make_move(game_id: int):
    with connections.cursor() as db:
        db.execute("""
        select game_expiration, game_phase, game_state
                   from game session
                   where game_id = %s
"""), (game_id)

def forfeit_game(session_id: uuid):
    try:
        with connections.cursor() as db:
            db.execute("""
                delete from game_session where session_id = %s;
            """, (session_id,))

        logging.info(f"Safely terminated session {session_id}")
    except Exception as e:
        logging.error('error on end_session', e)