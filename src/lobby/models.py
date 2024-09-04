from datetime import datetime
from typing import Optional, override

from app.exceptions import ValidationException
from app.str_tools import isBlank


class GameRequest:
    def __init__(self,data:dict):
        self.game_request_id: int= data.get('game_request_id')
        self.player_id: str = data.get('player_id')
        self.player_name: str = data.get('player_name')

    def json(self):
        return{
            'game_request_id': self.game_request_id,
            'player_id': self.player_id,
            'player_name': self.player_name
        }

class AvailablePlayerResponse:
    def __init__(self,data:dict):
        self.player_id: str = data.get('player_id')
        self.player_name: str = data.get('player_name')

        if self.player_id is None:
            raise Exception('player_id cannot be None')

        if self.player_name is None:
            raise Exception('player_name cannot be None')

    @override
    def validate(self): pass
    @override
    def copy(self, data: dict): pass

    @override
    def json(self):
        return{
            'player_id': self.player_id,
            'player_name': self.player_name
        }
