import logging
import uuid
from django_utils_morriswa.exceptions import BadRequestException
import datetime

from app import connections
from django.db import IntegrityError
from lobby.models import GameRequest, AvailablePlayerResponse


def get_available_players() -> list[AvailablePlayerResponse]:
    with connections.cursor() as db:
        db.execute("""
            select * 
            from player_slot slots
            left join user_session us
            on slots.player_id = us.player_id
            where slots.in_use = 'Y'
            and us.session_used between NOW() - INTERVAL '10 MINUTES' AND NOW();
        """)
        results = db.fetchall()
        return [AvailablePlayerResponse(result) for result in results]


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

def accept_match_request(player_id: int, game_request_id: int):

    with connections.cursor() as db:
        db.execute("""
            DO $$
            DECLARE
                player_invite_from char(4);
                player_invite_to char(4);
                num_ships char;
            BEGIN
                SELECT 
                    gr.player_invite_from,
                    gr.player_invite_to,
                    us.num_ships
                INTO 
                    player_invite_from,
                    player_invite_to,
                    num_ships
                FROM game_request gr
                left join user_session us 
                    on gr.player_invite_from = us.player_id
                WHERE 
                    gr.game_request_id = %s
                    and gr.player_invite_from = %s or gr.player_invite_to = %s;
                    
                insert into game_session
                    (game_id,
                    player_one_id, player_two_id,
                     active_turn, num_ships, 
                     game_phase, game_state)
                values
                    (%s,
                    player_invite_to, player_invite_from,
                    'p1', num_ships,
                    'selct','{}');
            END$$;   
        """, (game_request_id, player_id, player_id, uuid.uuid4()))

def request_random_match():
    raise NotImplementedError('please implement me!')

