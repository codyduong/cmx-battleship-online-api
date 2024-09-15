from datetime import datetime
from typing import Optional, override

from app.exceptions import ValidationException, APIException
from app.str_tools import isBlank

# This class is a model for active game request
class GameRequest:
    """ model for active game request """
    def __init__(self,data:dict):
        # Creates gamerequest with data from the dictionary 
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
        #Creates available player response with data from the dictionary 
        self.player_id: str = data.get('player_id')
        self.player_name: str = data.get('player_name')
        #Raises and exception if player_id is none
        if self.player_id is None:
            raise APIException('player_id cannot be None')
        #Raises and exception if player_name is none
        if self.player_name is None:
            raise APIException('player_name cannot be None')


    def json(self):
        #Returns a dictionary representation of the AvailablePlayerResponse
        return{
            'player_id': self.player_id,
            'player_name': self.player_name
        }
