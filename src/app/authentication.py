import uuid
import logging

from rest_framework.authentication import BaseAuthentication
from app import connections

class AuthenticatedPlayer:
    def __init__(self, data:dict):
        self.session_id = data.get('session_id')
        self.player_id = data.get('player_id')
        self.player_name = data.get('player_name')
        self.session_started = data.get('session_started')

        if self.session_id is None:
            raise RuntimeError('session_id required')

        if self.player_id is None:
            raise RuntimeError('player_id required')

        if self.player_name is None:
            raise RuntimeError('player_name required')

        if self.session_started is None:
            raise RuntimeError('session_started required')

        self.is_authenticated = True


class PlayerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.headers.get('session-id')
        if not session_id:
            return None

        player = authenticate_session(session_id)
        logging.info(f"Successfully authenticated as {player.player_name}#{player.player_id} with session {player.session_id}")
        return player, session_id


def authenticate_session(session_id: uuid) -> AuthenticatedPlayer:
    with connections.cursor() as db:
        db.execute("""select * from user_session where session_id = %s""", (session_id,))
        player_data = db.fetchone()
        if player_data is None:
            raise BadRequestException('invalid session')
        player = AuthenticatedPlayer(player_data)
        db.execute("""update user_session set session_used = current_timestamp where session_id = %s """, (session_id,))
        return player
