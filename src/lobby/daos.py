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
            select gr.player_invite_from as player_id,
                   us.player_name as player_name,
                   gr.game_request_id as game_request_id
                   from game_request gr 
                   left join user_session us
                   on gr.player_invite_from = us.player_id
                   where gr.player_invite_to = %s 
        """,(player_id,))

        db_result: list = db.fetchall()

        return [GameRequest(data) for data in db_result]
        
def create_game_request(current_player_id: str, requested_player_id: str):

    with connections.cursor() as db:
        request_create_time = datetime.datetime.now()
        request_expire_time = request_create_time + datetime.timedelta(minutes=10)

        db.execute("""
            INSERT INTO game_request
                (player_invite_from, player_invite_to, game_request_created, game_request_expiration) 
            VALUES (%s,%s,%s,%s)
        """, (current_player_id, requested_player_id, request_create_time, request_expire_time))
