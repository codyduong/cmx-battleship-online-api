import logging
from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_morriswa.exceptions import APIException, BadRequestException
from app.views import SessionView, session_view
from game.models import GameStateResponse, ActiveGameSession, GameState, Player, Play, other_player, GameBoard
import game.daos as game_dao


@session_view(['POST'])
def make_initial_move(request: Request) -> Response:

    initial_move = GameBoard(request.data)

    game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

    player_one_or_two: Player
    if game_session.player_one_id == request.user.player_id:
        player_one_or_two = 'p1'
    if game_session.player_two_id == request.user.player_id:
        player_one_or_two = 'p2'
    else:
        raise APIException('should only pull valid sessions...')

    if game_session.game_phase != 'selct':
        raise BadRequestException('you are no longer able to place or move ships!')

    game_state.setBoard(player_one_or_two, initial_move)

    if game_state.all_ships_placed():
        game_session.game_phase = 'goodg'
        game_session.active_turn = other_player(player_one_or_two)

    # game_session.game_state = game_state
    game_dao.submit_move(game_session)

    return Response(status=200, data=response)


class ActiveGameView(SessionView):

    @staticmethod
    def post(request: Request) -> Response:
        play = Play(request.data)
        game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

        player_one_or_two: Player
        if game_session.player_one_id == request.user.player_id:
            player_one_or_two = 'p1'
        if game_session.player_two_id == request.user.player_id:
            player_one_or_two = 'p2'
        else:
            raise APIException('should only pull valid sessions...')

        if game_session.active_turn != player_one_or_two:
            raise BadRequestException('not your turn!')

        game_state: GameState = game_session.game_state
        response = game_state.recordPlay(player_one_or_two, play)

        game_session.active_turn = other_player(player_one_or_two)
        # game_session.game_state = game_state
        game_dao.submit_move(game_session)

        return Response(status=200, data=response)

    # TODO implement forheit game
    # @staticmethod
    # def delete(request: Request) -> Response:
    #     game_dao.forfeit_game(request.user.session_id)
    #     return Response(status=204)
    