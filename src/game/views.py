import logging
from rest_framework.request import Request
from rest_framework.response import Response

from app.views import SessionView, session_view
import game.daos as game_dao

@session_view(['POST'])
def post_available_moves(request: Request) -> Response:
    moves = game_dao.post_available_moves()
    return Response(status=200, data=[moves.json() for move in moves])


class GameMovesView(SessionView):

    @staticmethod
    def post(request: Request) -> Response:
        #Need to edit logic?
        current_player_id = request.user.player_id
        requested_player_id = request.data.get('player_id')
        game_dao.create_game_request(current_player_id, requested_player_id)
        return Response(status = 204)
    
    @staticmethod
    #Need to edit logic?
    def delete(request: Request) -> Response:
        session_id = request.user.session_id
        if session_id is not None:
            game_dao.end_session(session_id)
        return Response(status=204)
    
    