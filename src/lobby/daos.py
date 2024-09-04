import logging
import uuid
from app.exceptions import BadRequestException
import datetime

from app import connections
from django.db import IntegrityError
from lobby.models import GameRequest, AvailablePlayerResponse


def get_available_players(session_id: uuid) -> list[AvailablePlayerResponse]:
    with connections.cursor() as db:
        db.execute("""
            select 
                slots.player_id,
                us.player_name
            from player_slot slots
            left join user_session us
            on slots.player_id = us.player_id
            where 
                slots.in_use = 'Y'
                and us.num_ships = (
                    select num_ships
                    from user_session
                    where session_id = %s
                    limit 1
                )
                and us.session_used between NOW() - INTERVAL '10 MINUTES' AND NOW();
        """, (session_id,))
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
        
def create_game_request(player_invite_from: str, player_invite_to: str):

    if player_invite_from == player_invite_to:
        raise BadRequestException('cannot request to match yourself')

    with connections.cursor() as db:
        db.execute("select 1 from game_request where player_invite_from = %s and player_invite_to = %s",
                   (player_invite_from, player_invite_to,))
        result = db.fetchone()
        if result is not None: return

        db.execute("""
            insert into game_request (player_invite_from, player_invite_to) 
            VALUES (%s, %s);
        """, (player_invite_from, player_invite_to,))

        db.execute("""
            delete from game_session
            where 
                player_one_id = %s 
                or player_two_id = %s;
        """, (player_invite_from, player_invite_from,))

def accept_match_request(player_id: int, game_request_id: int):

    with connections.cursor() as db:

        new_game_uuid = uuid.uuid4()

        db.execute("""
            SELECT 
                gr.player_invite_from,
                gr.player_invite_to,
                us.num_ships
            FROM game_request gr
            left join user_session us 
                on gr.player_invite_from = us.player_id
            WHERE 
                gr.game_request_id = %s
                and gr.player_invite_from = %s 
                or gr.player_invite_to = %s;
        """, (game_request_id, player_id, player_id,))
        result = db.fetchone()
        if result is None: raise BadRequestException('no such request')
        
        player_one_id = result.get('player_invite_to')
        player_two_id = result.get('player_invite_from')
        num_ships = result.get('num_ships')
        
        db.execute("""
            insert into game_session
                (game_id,
                player_one_id, player_two_id,
                 active_turn, num_ships, 
                 game_phase, game_state)
            values
                (%s,
                 %s, %s,
                'p1', %s,
                'selct','{}');
        """, (new_game_uuid, player_one_id, player_two_id, num_ships))

        db.execute("""             
            delete from game_request gr
            where gr.player_invite_from = %s
            or gr.player_invite_to = %s;
        """, (player_id, player_id))

def request_random_match():
    raise NotImplementedError('please implement me!')

