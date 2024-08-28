import uuid
from datetime import datetime
from typing import Optional, override

from django_utils_morriswa.exceptions import ValidationException
from django_utils_morriswa.models import DataModel
from django_utils_morriswa.str_tools import isBlank


class UserSession(DataModel):

    def __init__(self, data: dict):
        self.session_id: Optional[uuid] = data.get('session_id')
        self.player_id: Optional[str] = data.get('player_id')
        self.player_name: str = data.get('player_name')
        self.num_ships: str = data.get('num_ships')
        self.session_started: Optional[datetime] = data.get('session_started')
        self.session_used: Optional[datetime] = data.get('session_used')

        if self.player_name is None or isBlank(self.player_name):
            raise ValidationException(field='player_name', error='required')

        if self.num_ships is None or isBlank(self.num_ships):
            raise ValidationException(field='num_ships', error='required')

        self.validate()

    @override
    def validate(self):

        if len(self.player_name) < 4:
            raise ValidationException(field='player_name', error='min len 4')
        elif len(self.player_name) > 32:
            raise ValidationException(field='player_name', error='max len 32')

        if len(self.num_ships) != 1:
            raise ValidationException(field='num_ships', error='len 1')
        elif self.num_ships not in ['1', '2', '3', '4', '5']:
            raise ValidationException('num_ships', 'options 1-5')

    @override
    def copy(self, data: dict): pass

    @override
    def json(self): pass
