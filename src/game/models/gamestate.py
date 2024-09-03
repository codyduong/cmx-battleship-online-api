import json
import logging

from django_utils_morriswa.exceptions import BadRequestException

from .gameboard import GameBoard
from .validation import ensure_valid_tile_id


PLAYER_ONE = 'p1'
PLAYER_TWO = 'p2'
type Player = PLAYER_ONE | PLAYER_TWO
def other_player(player: Player) -> Player:
    if player == PLAYER_ONE:
        return PLAYER_TWO
    if player == PLAYER_TWO:
        return PLAYER_ONE
    else: raise ValueError(f'invalid player {player}')

class GameStateResponse:
    def __init__(self, hit_tile_ids: list[str], miss_tile_ids: list[str], enemy_ships_remaining: int):
        self.hit_tile_ids = hit_tile_ids
        self.miss_tile_ids = miss_tile_ids
        self.enemy_ships_remaining = enemy_ships_remaining



class GameState:
    def __init__(self, json_data: str):
        json_obj = json.loads(json_data)
        self.p1_attacks: list[str] = json_obj.get('p1_attacks')
        self.p2_attacks: list[str] = json_obj.get('p2_attacks')

        p1boardState = json_obj.get('p1_board')
        p2boardState = json_obj.get('p2_board')
        self.p1_board: Optional[GameBoard] = GameBoard(p1boardState) \
            if p1boardState is not None else None
        self.p2_board: Optional[GameState] = GameBoard(p2boardState) \
            if p2boardState is not None else None

        self.validate()


    # getters
    def getState(self, player: Player) -> GameStateResponse:
        return self._get_state(player)

    def json(self) -> dict:

        self.validate()

        json_str = {
            'p1_attacks': self.p1_attacks,
            'p2_attacks': self.p2_attacks,
            'p1_board': self.p1_board.json(),
            'p2_board': self.p2_board.json()
        }
        logging.info(f'saved state as {json_str}')

        return json_str

    def all_ships_placed(self) -> bool:
        return self.p1_board is not None and self.p2_board is not None


    # setters
    def setBoard(self, player: Player, valid_board: GameBoard):
        if getattr(self, f'{player}_board') is not None:
            raise BadRequestException('can only place ships once')

        setattr(self, f'{player}_board', valid_board)

    def recordPlay(self, player_id: str, tile_id: str) -> GameStateResponse:
        return self._record_play(player_id, tile_id)


    # state
    def validate(self):
        if self.p1_board is not None: self.p1_board.validate()
        if self.p2_board is not None: self.p2_board.validate()
        if self.p1_board is not None and self.p2_board is not None:
            if self.p1_board.ship_count() != self.p2_board.ship_count():
                raise BadRequestException('players should only be assigned to players with a similar sized board')


    # internal
    def _get_state(self, player: str):
        player_attacks = getattr(self, f'{player}_attacks')

        other_player = 'p1' if player == 'p2' else 'p2'
        other_player_board: GameBoard = getattr(self, f'{other_player}_board')

        hit_tile_ids = [tile_id
            for tile_id in player_attacks
            if tile_id in other_player_board.all_tiles()
        ]

        miss_tile_ids = [tile_id
            for tile_id in player_attacks
            if tile_id not in hit_tile_ids
        ]

        enemy_ships_remaining = 0
        for ship in other_player_board.ships():
            sunk = True
            for tile_id in hit_tile_ids:
                if tile_id not in ship:
                    sunk = False

            if not sunk:
                enemy_ships_remaining += 1

        return GameStateResponse(hit_tile_ids, miss_tile_ids, enemy_ships_remaining)

    def _record_play(self, player, tile_id: str):
        ensure_valid_tile_id(tile_id)
        player_attacks: list[str] = getattr(self, f'{player}_attacks')
        if tile_id in player_attacks:
            raise ValidationException('tile_id', 'you have already struck this tile')

        player_attacks.append(tile_id)

        return self._get_state(player)
