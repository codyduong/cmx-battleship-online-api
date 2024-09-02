from django.test import TestCase
from django.conf import settings

from game.models import GameState

class GameStateModelsTest(TestCase):
    def test_create_state_from_json(self):
        json = """{
            "p1attacks": ["A1"],
            "p2attacks": ["B2"],
            "p1board": {
                "ship1": ["C1"]
            },
            "p2board": {
                "ship1": ["D1"]
            }
        }"""

        state = GameState(json)
        self.assertEqual(state.p1attacks[0], 'A1', 'should match json')
        self.assertEqual(state.p1board.ship1[0], 'A1', 'should match json')
