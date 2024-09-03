from django_utils_morriswa.exceptions import BadRequestException, ValidationException

from .validation import ensure_valid_ship_row


class GameBoard:
    def __init__(self, json_data: dict):
        self.ship_1 = json_data.get('ship_1')
        self.ship_2 = json_data.get('ship_2')
        self.ship_3 = json_data.get('ship_3')
        self.ship_4 = json_data.get('ship_4')
        self.ship_5 = json_data.get('ship_5')

        self.validate()

    def all_tiles(self):
        all_tiles = []
        for ship_num in range(1, 6):
            ship_name = f'ship_{ship_num}'
            current_ships = getattr(self, ship_name)
            if current_ships is None: break
            for tile in current_ships:
                all_tiles.append(tile)

        return all_tiles

    def ships(self):
        ships = []
        for ship_num in range(1, 6):
            ship_name = f'ship_{ship_num}'
            current_ships = getattr(self, ship_name)
            if current_ships is None: break
            ships.append(current_ships)

        return ships

    def validate(self):
        ship_num: int
        count = 0
        all_tiles = []
        for ship_num in range(1, 6):
            ship_name = f'ship_{ship_num}'
            current_ship = getattr(self, ship_name)
            if current_ship is None:
                break

            if len(current_ship) != ship_num:
                raise ValidationException(ship_name, f'must have {ship_num} ships, found {count}')

            count += 1

            ensure_valid_ship_row(ship_num, current_ship)

            for tile in current_ship:
                all_tiles.append(tile)

        for remaining in range(count + 1, 6):
            setattr(self, f'ship_{remaining}', None)

        for tile in all_tiles:
            if all_tiles.count(tile) > 1:
                raise BadRequestException('no overlapping ships')

    def ship_count(self) -> int:
        return len(self.ships())

    def json(self) -> dict:
        self.validate()
        return {
            'ship_1': self.ship_1,
            'ship_2': self.ship_2,
            'ship_3': self.ship_3,
            'ship_4': self.ship_4,
            'ship_5': self.ship_5
        }
