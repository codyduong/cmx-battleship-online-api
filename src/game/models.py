import json
import logging

from django_utils_morriswa.models import DataModel
from django_utils_morriswa.exceptions import ValidationException, BadRequestException


VALID_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
VALID_ROWS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


def _valid_tile_id(tile: str) -> (str, str):
    col = tile[0]
    row = tile[1::]
    if col not in VALID_COLUMNS:
        raise BadRequestException('invalid column identifier')

    if row not in VALID_ROWS:
        raise BadRequestException('invalid row identifier')

    return (col, row)

def _valid_ship_row(ship_len: int, ship_collection: list[str]):
    last_col: str = None
    last_row: str = None
    for tile in ship_collection:
        if last_col is None and last_row is None:
            (last_col, last_row) = _valid_tile_id(tile)
        else:
            (col, row) = _valid_tile_id(tile)

            if col != last_col and row != last_row:
                raise ValidationException(f'ship{ship_len}', 'ships must share similar row or column ie no diagonals')
            elif (col != last_col and row == last_row
                  and col != VALID_COLUMNS[VALID_COLUMNS.index(last_col) - 1]
                  and col != VALID_COLUMNS[VALID_COLUMNS.index(last_col) + 1]):
                    raise ValidationException(f'ship{ship_len}',
                                              'ships must share at least 1 border')
            elif (col == last_col and row != last_row
                  and row != VALID_ROWS[VALID_ROWS.index(last_row) - 1]
                  and row != VALID_ROWS[VALID_ROWS.index(last_row) + 1]):
                    raise ValidationException(f'ship{ship_len}',
                                              'ships must share at least 1 border')

            last_col = col
            last_row = row



class GameBoard:
    def __init__(self, json_data: dict):
        self.ship1 = json_data.get('ship1')
        self.ship2 = json_data.get('ship2')
        self.ship3 = json_data.get('ship3')
        self.ship4 = json_data.get('ship4')
        self.ship5 = json_data.get('ship5')

        self.validate()

    def all_tiles(self):
        ship_num: int
        all_tiles = []
        for ship_num in range(1, 6):
            ship_name = f'ship{ship_num}'
            current_ship = getattr(self, ship_name)

            if current_ship is None: break

            for tile in current_ship:
                all_tiles.append(tile)

        return all_tiles

    def ships(self):
        ships = []
        for ship_num in range(1, 6):
            ship_name = f'ship{ship_num}'
            current_ship = getattr(self, ship_name)
            if current_ship is None: break
            ships.append(current_ship)

        return ships

    def validate(self):
        ship_num: int
        count = 0
        all_tiles = []
        for ship_num in range(1, 6):
            ship_name = f'ship{ship_num}'
            current_ship = getattr(self, ship_name)
            if current_ship is None:
                break

            if len(current_ship) != ship_num:
                raise ValidationException(ship_name, f'must have {ship_num} ships, found {count}')

            count += 1

            _valid_ship_row(ship_num, current_ship)

            for tile in current_ship:
                all_tiles.append(tile)

        for remaining in range(count + 1, 6):
            setattr(self, f'ship{remaining}', None)

        for tile in all_tiles:
            if all_tiles.count(tile) > 1:
                raise BadRequestException('no overlapping ships')

    def ship_count(self) -> int:
        return len(self.ships())

    def json(self) -> dict:
        self.validate()
        return {
            'ship1': self.ship1,
            'ship2': self.ship2,
            'ship3': self.ship3,
            'ship4': self.ship4,
            'ship5': self.ship5
        }


class GameStateResponse:
    def __init__(self, hit_tile_ids: list[str], miss_tile_ids: list[str], enemy_ships_remaining: int):
        self.hit_tile_ids = hit_tile_ids
        self.miss_tile_ids = miss_tile_ids
        self.enemy_ships_remaining = enemy_ships_remaining


class GameState:
    def __init__(self, json_data: str):
        json_obj = json.loads(json_data)
        self.p1attacks: list[str] = json_obj.get('p1attacks')
        self.p2attacks: list[str] = json_obj.get('p2attacks')

        p1boardState = json_obj.get('p1board')
        p2boardState = json_obj.get('p2board')
        self.p1board: Optional[GameBoard] = GameBoard(p1boardState) \
            if p1boardState is not None else None
        self.p2board: Optional[GameState] = GameBoard(p2boardState) \
            if p2boardState is not None else None

        self.validate()

    def setP1board(self, valid_board: GameBoard):
        self.p1board = valid_board

    def setP2board(self, valid_board: GameBoard):
        self.p2board = valid_board

    def getP1state(self) -> GameStateResponse:
        return self._get_state('p1')

    def getP2state(self) -> GameStateResponse:
        return self._get_state('p2')

    def recordP1play(self, tile_id: str) -> GameStateResponse:
        return self._record_play('p1', tile_id)

    def recordP2play(self, tile_id: str) -> GameStateResponse:
        return self._record_play('p2', tile_id)

    def json(self) -> dict:

        self.validate()

        json_str = {
            'p1attacks': self.p1attacks,
            'p2attacks': self.p2attacks,
            'p1board': self.p1board.json(),
            'p2board': self.p2board.json()
        }
        logging.info(f'saved state as {json_str}')

        return json_str

    def validate(self):
        if self.p1board is not None: self.p1board.validate()
        if self.p2board is not None: self.p2board.validate()
        if self.p1board is not None and self.p2board is not None:
            if self.p1board.ship_count() != self.p2board.ship_count():
                raise BadRequestException('players should only be assigned to players with a similar sized board')

    # internal
    def _get_state(self, player: str):
        player_attacks = getattr(self, f'{player}attacks')

        other_player = 'p1' if player == 'p2' else 'p2'
        other_player_board: GameBoard = getattr(self, f'{other_player}board')

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
        _valid_tile_id(tile_id)
        player_attacks: list[str] = getattr(self, f'{player}attacks')
        if tile_id in player_attacks:
            raise ValidationException('tile_id', 'you have already struck this tile')

        player_attacks.append(tile_id)

        return self._get_state(player)
