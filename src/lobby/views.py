from rest_framework.request import Request
from rest_framework.response import Response

import lobby.daos as lobby_dao

from app.utils import AnyView, WView


class GameRequestView(WView):
    @staticmethod
    def get(request: Request) -> Response:
        session_id = request.user.session_id
        requests = lobby_dao.get_game_request(session_id)
        return Response(status = 200,data = [request.json() for request in requests])
    
    @staticmethod
    def post(request: Request) -> Response:
        session_id = request.user.session_id
        player_id = request.data.get('player_id')
        lobby_dao.create_game_request(session_id, player_id)
        return Response(status = 204)
