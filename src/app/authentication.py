import uuid
import logging
from typing import override

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

import user_session.daos as user_session_dao


class PlayerAuthentication(BaseAuthentication):
    """ provides a django authentication class that verifies a request contains a valid session header """

    @override
    @staticmethod
    def authenticate(request):
        """ override authenticate fn to provide custom auth logic"""

        # retrieve session-id header
        session_id = request.headers.get('session-id')
        if not session_id:
            # if no session id header was found, raise error
            raise AuthenticationFailed("failed to provide required header 'session-id'")

        # attempt to retrieve session
        player = user_session_dao.retrieve_session(session_id)
        if not player:  # raise error if no sessino is found
            raise AuthenticationFailed("invalid session, please log in again")
        else:  # return authenticated player if session was valid
            logging.info(
                f"Successfully authenticated as {player.player_name}#{player.player_id} with session {player.session_id}")

            return player, session_id
