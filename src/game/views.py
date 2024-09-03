import logging
from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_morriswa.exceptions import APIException, BadRequestException
from app.views import SessionView, session_view
from game.models import GameStateResponse, ActiveGameSession, GameState, Player, Play, PLAYER_ONE, PLAYER_TWO, other_player, GameBoard
import game.daos as game_dao


@session_view(['POST'])
def make_initial_move(request: Request) -> Response:

    initial_move: GameBoard = GameBoard(request.data)

    game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

    player_one_or_two: Player
    if game_session.player_one_id == request.user.player_id:
        player_one_or_two = 'p1'
    elif game_session.player_two_id == request.user.player_id:
        player_one_or_two = 'p2'
    else:
        raise APIException('should only pull valid sessions...')

    if game_session.game_phase != 'selct':
        raise BadRequestException('you are no longer able to place or move ships!')

    game_state: GameState = game_session.game_state
    game_state.set_board(player_one_or_two, initial_move)

    if game_state.all_ships_placed():
        logging.info('send all ships placed signal')
        game_session.game_phase = 'goodg'
        game_session.active_turn = other_player(player_one_or_two)

    game_session.game_state = game_state

    # game_session.game_state = game_state
    game_dao.submit_move(game_session)

    return Response(status=204)


class ActiveGameView(SessionView):

    @staticmethod
    def get(request: Request) -> Response:
        game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

        if game_session is None: return Response(status=200)

        player_one_or_two: Player
        if game_session.player_one_id == request.user.player_id:
            player_one_or_two = 'p1'
        elif game_session.player_two_id == request.user.player_id:
            player_one_or_two = 'p2'
        else:
            raise APIException('should only pull valid sessions...')

        game_state: GameState = game_session.game_state

        if game_state.all_ships_placed() and game_session.game_phase == 'selct':
            game_dao.submit_move(game_session)

        game_state_response = game_state.getState(player_one_or_two)

        game_state_json: Optional[str]
        if game_state_response is None:
            game_state_json = None
        else:
            game_state_json = game_state_response.json()

        return Response(status=200, data={
            'player_id': request.user.player_id,
            'opponent_id': game_session.player_two_id
                if player_one_or_two == PLAYER_ONE else game_session.player_one_id,
            'active_turn': game_session.active_turn,
            'oppenent_name': None,
            'game_timeout': None,
            'game_phase': game_session.game_phase,
            'player_one_or_two': player_one_or_two,
            'game_state': game_state_json
        })

    @staticmethod
    def post(request: Request) -> Response:
        play = Play(request.data)
        game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

        player_one_or_two: Player
        if game_session.player_one_id == request.user.player_id:
            player_one_or_two = 'p1'
        elif game_session.player_two_id == request.user.player_id:
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

    @staticmethod
    def delete(request: Request) -> Response:
        game_dao.forfeit_game(request.user.session_id)
        return Response(status=204)
    