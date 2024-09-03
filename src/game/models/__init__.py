import json
import logging

from django_utils_morriswa.models import DataModel

from .gameboard import *;
from .gamestate import *;
from .validation import *;

class ActiveGameSession:
    def __init__(self, data: dict):
        self.game_id = data.get('game_id')
        self.player_one_id = data.get('player_one_id')
        self.player_two_id = data.get('player_two_id')
        self.active_turn = data.get('active_turn')
        self.num_ships = data.get('num_ships')
        self.game_started = data.get('game_started')
        self.game_phase = data.get('game_phase')
        self.game_state: GameState = GameState(data.get('game_state'))


class Play:
    def __init__(self, data: dict):
        self.tile_id = data.get('tile_id')

        if self.tile_id is None:
            raise ValidationException('tile_id', 'is required')