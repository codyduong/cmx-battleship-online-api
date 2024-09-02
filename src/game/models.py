import json

from django_utils_morriswa.models import DataModel

from app.utils import parse_json


class GameState:
    def __init__(self, json_data: str):
        json_obj = json.loads(json_data)
        self.p1attacks: list[str] = json_obj.get('p1attacks')
        self.p2attacks: list[str] = json_obj.get('p2attacks')
        self.p1board: GameState = GameBoard(json_obj.get('p1board'))
        self.p2board: GameState = GameBoard(json_obj.get('p2board'))


class GameBoard:
    def __init__(self, json: any):
        self.ship1 = json.get('ship1') or []
        self.ship2 = json.get('ship2') or []
        self.ship3 = json.get('ship3') or []
        self.ship4 = json.get('ship4') or []
        self.ship5 = json.get('ship5') or []
