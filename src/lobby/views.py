import logging
from rest_framework.request import Request
from rest_framework.response import Response

from app.views import SessionView
from app.decorators import session_view

import lobby.daos as lobby_dao


@session_view(['GET'])
def get_available_players(request: Request) -> Response:
    """ returns list of all available players in requested lobby, excluding requestor """
    players = lobby_dao.get_available_players(request.user.session_id)
    return Response(status=200, data=[player.json()
        for player in players
        if player.player_id != request.user.player_id
    ])



class GameRequestView(SessionView):

    @staticmethod
    def get(request: Request) -> Response:
        """ returns all game requests from other players """
        player_id = request.user.player_id
        requests = lobby_dao.get_game_requests(player_id)
        return Response(status = 200, data = [request.json() for request in requests])
    
    @staticmethod
    def post(request: Request) -> Response:
        """ creates a game request to player with specified player_id """
        current_player_id = request.user.player_id
        requested_player_id = request.data.get('player_id')
        lobby_dao.create_game_request(current_player_id, requested_player_id)
        return Response(status = 204)
    

@session_view(['POST'])
def accept_match_request(request: Request, game_request_id: int) -> Response:
    """ accept pending match request """
    lobby_dao.accept_match_request(request.user.player_id, game_request_id)
    return Response(status = 204)
