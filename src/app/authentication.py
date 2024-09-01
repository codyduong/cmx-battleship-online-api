import uuid
import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from app import connections
import user_session.daos as user_session_dao


class PlayerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.headers.get('session-id')
        if not session_id:
            return None

        player = user_session_dao.authenticate_session(session_id)
        logging.info(f"Successfully authenticated as {player.player_name}#{player.player_id} with session {player.session_id}")
        return player, session_id
