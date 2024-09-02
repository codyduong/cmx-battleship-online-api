import logging
from rest_framework.request import Request
from rest_framework.response import Response

from app.views import SessionView, session_view
import lobby.daos as lobby_dao


@session_view(['GET'])
def get_available_players(request: Request) -> Response:
    players = lobby_dao.get_available_players()
    return Response(status=200, data=[player.json() for player in players])



class GameRequestView(SessionView):

    @staticmethod
    def get(request: Request) -> Response:
        player_id = request.user.player_id
        requests = lobby_dao.get_game_requests(player_id)
        return Response(status = 200, data = [request.json() for request in requests])
    
    @staticmethod
    def post(request: Request) -> Response:
        current_player_id = request.user.player_id
        requested_player_id = request.data.get('player_id')
        lobby_dao.create_game_request(current_player_id, requested_player_id)
        return Response(status = 204)
    


class MatchRequestView(SessionView):

    @staticmethod
    def post(request: Request) -> Response:
        game_request_id = request.query.get('gameRequestId')
        current_player_id = request.user.player_id
        request_player_id = request.data.get('player_id')
        lobby_dao.accept_match_request(game_request_id, current_player_id, request_player_id)
        return Response(status = 204)

class GameStatusView(SessionView):
    @staticmethod 
    def get(request:Request) -> Response:
        player_one_id = request.user.get('player_one_id')
        player_two_id = request.user.get('player_two_id')
        game_expiration = request.user.get('game_expiration') 
        game_phase = 
        game_state = 