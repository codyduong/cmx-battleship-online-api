import logging
import uuid
import json
from typing import Optional

from app.exceptions import BadRequestException

from app import connections
from .models import ActiveGameSession


def retrieve_active_game_session(player_id: str) -> Optional[ActiveGameSession]:
    with connections.cursor() as db:
        #Execute the query to get the game session for player1 or player2
        db.execute("""
            select *
            from game_session 
            where 
                player_one_id = %s
                or player_two_id = %s
        """, (player_id, player_id,))
        result = db.fetchone()
        # if result is None:
        #     raise BadRequestException('failed to locate game session')
        return ActiveGameSession(result) if result is not None else None

def save_active_game_session(game_session: ActiveGameSession) -> ActiveGameSession:
    with connections.cursor() as db:
        #Execute the query to updte the game session
        db.execute("""
            update game_session
            set
                game_state = %s,
                active_turn = %s,
                game_phase = %s,
                last_play = current_timestamp
            where game_id = %s;
        """, (
            json.dumps(game_session.game_state.json()),
            game_session.active_turn,
            game_session.game_phase,
            game_session.game_id,
        ))


def delete_active_game_session(player_id: str):
    try:
        with connections.cursor() as db:
            #Execute the query to delete the game session
            db.execute("""
                
                delete from game_session
                where
                    player_one_id = %s
                    or player_two_id = %s;
            """, (player_id,player_id,))

    except Exception as e:
        #Logs any errors that occur during the deletion of the game session
        logging.error('error on delete_active_game_session')