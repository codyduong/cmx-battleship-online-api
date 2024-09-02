import logging
import uuid
from app import connections

def init_move(state: object):
    try:
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