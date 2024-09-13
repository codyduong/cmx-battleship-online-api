from datetime import datetime
from typing import Optional, override

from app.exceptions import ValidationException, APIException
from app.str_tools import isBlank


class GameRequest:
    """ model for active game request """
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
    """ model for available player """
    def __init__(self,data:dict):
        self.player_id: str = data.get('player_id')
        self.player_name: str = data.get('player_name')

        if self.player_id is None:
            raise APIException('player_id cannot be None')

        if self.player_name is None:
            raise APIException('player_name cannot be None')


    def json(self):
        return{
            'player_id': self.player_id,
            'player_name': self.player_name
        }
