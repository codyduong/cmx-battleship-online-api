import logging
import uuid

from django_utils_morriswa.exceptions import BadRequestException

from app import connections
from .models import ActiveGameSession


def retrieve_active_game_session(player_id: str) -> ActiveGameSession:
    with connections.cursor() as db:
        db.execute("""
            select *
            from game_session 
            where 
                player_one_id = %s
                or player_two_id = %s
        """, (player_id, player_id,))
        result = db.fetchone()
        if result is None:
            raise BadRequestException('failed to locate game session')
        return GameSession(result)

def submit_move(game_session: ActiveGameSession) -> ActiveGameSession:
    with connections.cursor() as db:
        db.execute("""
            update game_session
            set
                game_state = %s,
                active_turn = %s,
                last_play = current_timestamp
            where game_id = %s;
        """, (
            game_session.game_state.json(),
            game_session.active_turn,
            game_session.game_id,
        ))
        result = db.fetchone()
        if result is None:
            raise BadRequestException('failed to locate game session')
        return GameSession(result)


def forfeit_game(session_id: uuid):
    try:
        with connections.cursor() as db:
            db.execute("""
                delete from game_session where session_id = %s;
            """, (session_id,))

        logging.info(f"Safely terminated session {session_id}")
    except Exception as e:
        logging.error('error on end_session', e)