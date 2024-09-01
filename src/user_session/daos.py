import logging
import uuid
from django_utils_morriswa.exceptions import BadRequestException
import datetime

from app import connections
from django.db import IntegrityError
from user_session.models import LoginRequest


def get_online_player_count() -> int:
    count: int
    with connections.cursor() as db:
        db.execute("""
            -- delete unused rows
            delete from user_session where session_used not between NOW() - INTERVAL '10 MINUTES' AND NOW();
            -- and count remaining players
            select count(player_id) as online_player_count from player_slot where in_use = 'Y';
        """)
        count = db.fetchone()['online_player_count']

    return count

def get_valid_id() -> str:
    player_id: str
    with connections.cursor() as db:
        db.execute("select player_id from player_slot where in_use = 'N' limit 1")
        player_id = db.fetchone()['player_id']

    return player_id

def start_session(session: LoginRequest) -> dict:
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
    except Exception as e:
        logging.error('error on start_session', e)


def end_session(session_id: uuid) -> dict:
    try:
        with connections.cursor() as db:
            db.execute("""
                delete from user_session where session_id = %s;
            """, (session_id,))
    except Exception as e:
        logging.error('error on end_session', e)
