from datetime import datetime
from typing import Optional, override

from django_utils_morriswa.exceptions import ValidationException
from django_utils_morriswa.models import DataModel
from django_utils_morriswa.str_tools import isBlank


class GameRequest(DataModel):
    def __init__(self,data:dict):
        self.game_request_id: int= data.get('game_request_id')
        self.player_id: str = data.get('player_id')
        self.player_name: str = data.get('player_name')

    @override
    def validate(self): pass
    @override
    def copy(self, data: dict): pass

    @override
    def json(self):
        return{
            'game_request_id': self.game_request_id,
            'player_id': self.player_id,
            'player_name': self.player_name
        }
