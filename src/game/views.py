import logging
from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response

from app.exceptions import APIException, BadRequestException
from app.views import SessionView
from app.decorators import session_view
from game.models import GameStateResponse, ActiveGameSession, GameState, Player, Play, PLAYER_ONE, PLAYER_TWO, other_player, GameBoard
import game.daos as game_dao


@session_view(['POST'])
def make_initial_move(request: Request) -> Response:
    """ endpoint to submit ship placement, performs input validation """

    # create gameboard from request body
    initial_move: GameBoard = GameBoard(request.data)

    # retrieve existing game session
    game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

    # determine whether logged in player is p1 or p2
    player_one_or_two: Player
    if game_session.player_one_id == request.user.player_id:
        player_one_or_two = 'p1'
    elif game_session.player_two_id == request.user.player_id:
        player_one_or_two = 'p2'
    else:  # should always be p1 or p2, else throw an error
        raise APIException('should only pull valid sessions...')

    if game_session.game_phase != 'selct':  # if game is not in SELECTION phase, this endpoint cannot be called
        raise BadRequestException('you are no longer able to place or move ships!')

    if game_session.game_state is None:
        logging.error('bad')

    # and set current player board
    game_session.game_state.set_board(player_one_or_two, initial_move)

    # if p1 and p2 have submitted their ship placement
    if game_session.game_state.all_ships_placed():
        game_session.game_phase = 'goodg'  # change game phase to GOOD_GAME
        game_session.active_turn = other_player(player_one_or_two)  # set active turn to opposite player

    # update game session
    game_dao.save_active_game_session(game_session)

    # no content on success
    return Response(status=204)


class ActiveGameView(SessionView):

    @staticmethod
    def get(request: Request) -> Response:
        """ returns an active game session for the current player """

        game_session: ActiveGameSession = game_dao.retrieve_active_game_session(request.user.player_id)

        # return blank if no session is found
        if game_session is None: return Response(status=200)

        # determine if current player is p1 or p2
        player_one_or_two: Player
        if game_session.player_one_id == request.user.player_id:
            player_one_or_two = 'p1'
        elif game_session.player_two_id == request.user.player_id:
            player_one_or_two = 'p2'
        else:
            raise APIException('should only pull valid sessions...')

        # if all selections were made, but game is still in SELECT phase, transition to GOOD_GAME phase
        if ((game_session.game_state.all_ships_placed() and game_session.game_phase == 'selct')
                or game_session.game_state.gen_game_phase() != 'goodg'):
            game_session.game_phase = game_session.game_state.gen_game_phase();
            game_dao.save_active_game_session(game_session)

        # retrieve game state for current player, hiding data about other player
        game_state_response = game_session.game_state.getState(player_one_or_two)
        game_state_json: Optional[str]
        # only return game state info if game state exists
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
        """ logs a player attack on opponent board """
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

        # game_state: GameState = game_session.game_state
        response = game_session.game_state.recordPlay(player_one_or_two, play)

        game_session.game_phase = game_session.game_state.gen_game_phase()

        game_session.active_turn = other_player(player_one_or_two)
        # game_session.game_state = game_state
        game_dao.save_active_game_session(game_session)

        return Response(status=200, data=response.json())

    @staticmethod
    def delete(request: Request) -> Response:
        game_dao.delete_active_game_session(request.user.player_id)
        return Response(status=204)
    