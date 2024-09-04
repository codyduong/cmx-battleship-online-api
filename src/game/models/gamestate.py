import json
import logging
from typing import Optional

from django_utils_morriswa.exceptions import BadRequestException, ValidationException

from .gameplay import Play, Player, PLAYER_TWO, PLAYER_ONE
from .gameboard import GameBoard
from .validation import ensure_valid_tile_id


type GamePhase = 'selct' | 'p1win' | 'p2win' | 'nowin' | 'goodg'

def other_player(player: Player) -> Player:
    if player == PLAYER_ONE:
        return PLAYER_TWO
    if player == PLAYER_TWO:
        return PLAYER_ONE
    else: raise ValueError(f'invalid player {player}')



class GameStateResponse:
    def __init__(self,
                 hit_tile_ids: list[str], miss_tile_ids: list[str], ships_remaining: int,
                 my_hit_tile_ids: list[str], my_miss_tile_ids: list[str], my_ships_remaining: int):
        self.hit_tile_ids = hit_tile_ids
        self.miss_tile_ids = miss_tile_ids
        self.ships_remaining = ships_remaining
        self.my_hit_tile_ids = my_hit_tile_ids
        self.my_miss_tile_ids = my_miss_tile_ids
        self.my_ships_remaining = my_ships_remaining

    def json(self):
        return {
            'hit_tile_ids': self.hit_tile_ids,
            'miss_tile_ids': self.miss_tile_ids,
            'ships_remaining': self.ships_remaining,
            'my_hit_tile_ids': self.my_hit_tile_ids,
            'my_miss_tile_ids': self.my_miss_tile_ids,
            'my_ships_remaining': self.my_ships_remaining,
        }



class GameState:
    def __init__(self, json_data: str):
        json_obj = json.loads(json_data)
        self.p1_attacks: list[str] = json_obj.get('p1_attacks') or []
        self.p2_attacks: list[str] = json_obj.get('p2_attacks') or []

        p1boardState = json_obj.get('p1_board')
        p2boardState = json_obj.get('p2_board')
        self.p1_board: Optional[GameBoard] = GameBoard(p1boardState) \
            if p1boardState is not None else None
        self.p2_board: Optional[GameBoard] = GameBoard(p2boardState) \
            if p2boardState is not None else None

        self.validate()


    # getters
    def gen_game_phase(self) -> GamePhase:

        if self.p1_board is None or self.p2_board is None:
            return 'selct'

        p1_ship_counter = self._get_state('p1').my_ships_remaining
        p2_ship_counter = self._get_state('p2').my_ships_remaining
        if p1_ship_counter == 0: return 'p2win'
        if p2_ship_counter == 0: return 'p1win'

        return 'goodg'


    def getState(self, player: Player) -> GameStateResponse:
        return self._get_state(player)

    def json(self) -> dict:

        self.validate()

        json_str: dict = {
            'p1_attacks': self.p1_attacks,
            'p2_attacks': self.p2_attacks,
        }

        if self.p1_board is not None:
            json_str['p1_board'] = self.p1_board.json()

        if self.p2_board is not None:
            json_str['p2_board'] = self.p2_board.json()

        return json_str

    def all_ships_placed(self) -> bool:
        return self.p1_board is not None and self.p2_board is not None


    # setters
    def set_board(self, player: Player, valid_board: GameBoard):
        if getattr(self, f'{player}_board') is not None:
            raise BadRequestException('can only place ships once')

        setattr(self, f'{player}_board', valid_board)
        self.validate()

    def recordPlay(self, player_id: Player, play: Play) -> GameStateResponse:
        return self._record_play(player_id, play.tile_id)


    # state
    def validate(self):
        if self.p1_board is not None: self.p1_board.validate()
        if self.p2_board is not None: self.p2_board.validate()
        if self.p1_board is not None and self.p2_board is not None:
            if self.p1_board.ship_count() != self.p2_board.ship_count():
                raise BadRequestException('players should only be assigned to players with a similar sized board')


    # internal
    def _get_state(self, player: str):

        other_player = 'p1' if player == 'p2' else 'p2'

        player_board: Optional[GameBoard] = getattr(self, f'{player}_board')
        player_attacks: list[str] = getattr(self, f'{player}_attacks')
        other_player_board: Optional[GameBoard] = getattr(self, f'{other_player}_board')
        other_player_attacks: list[str] = getattr(self, f'{other_player}_attacks')


        if player_board is not None and other_player_board is None:
            return GameStateResponse([], [], None,
                                     [], player_board.all_tiles(), player_board.ship_count())

        elif player_board is None or other_player_board is None:
            return None


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
            for tile_id in ship:
                if tile_id not in hit_tile_ids:
                    sunk = False

            if not sunk:
                enemy_ships_remaining += 1

        my_hit_tile_ids = [tile_id
            for tile_id in other_player_attacks
            if tile_id in player_board.all_tiles()
        ]

        my_miss_tile_ids = [tile_id
            for tile_id in player_board.all_tiles()
            if tile_id not in my_hit_tile_ids
        ]

        my_ships_remaining = 0
        for ship in player_board.ships():
            sunk = True
            for tile_id in ship:
                if tile_id not in my_hit_tile_ids:
                    sunk = False

            if not sunk:
                my_ships_remaining += 1

        return GameStateResponse(hit_tile_ids, miss_tile_ids, enemy_ships_remaining,
                                 my_hit_tile_ids, my_miss_tile_ids, my_ships_remaining)

    def _record_play(self, player: Player, tile_id: str):
        ensure_valid_tile_id(tile_id)
        player_attacks: list[str] = getattr(self, f'{player}_attacks')
        if tile_id in player_attacks:
            raise ValidationException('tile_id', 'you have already struck this tile')

        player_attacks.append(tile_id)

        return self._get_state(player)
