
class Play:
    def __init__(self, data: dict):
        self.tile_id = data.get('tile_id')

        if self.tile_id is None:
            raise ValidationException('tile_id', 'is required')

PLAYER_ONE = 'p1'
PLAYER_TWO = 'p2'
type Player = PLAYER_ONE | PLAYER_TWO
