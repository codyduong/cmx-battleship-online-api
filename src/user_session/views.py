from rest_framework.request import Request
from rest_framework.response import Response
from user_session.models import UserSession

import user_session.daos as user_session_dao

from app.utils import AnyView


class UserSessionView(AnyView):

    @staticmethod
    def post(request: Request) -> Response:
        create_session_repr = UserSession(request.data)
        session_info = user_session_dao.start_session(create_session_repr)
        return Response(status=200, data=session_info)

    @staticmethod
    def delete(request: Request) -> Response:
        session_id = request.data.get('session_id')
        if session_id is not None:
            user_session_dao.end_session(session_id)
        return Response(status=204)



class GameRequestView(AnyView):
    @staticmethod
    def get(request: Request) -> Response:
        session_id = request.data.get('session_id')
        requests = user_session_dao.get_game_request(session_id)
        return Response(status = 200,data = [request.json() for request in requests])
    
    @staticmethod
    def post(request: Request) -> Response:
        session_id = request.data.get('session_id')
        player_id = request.data.get('player_id')
        user_session_dao.create_game_request(session_id, player_id)
        return Response(status = 204)

