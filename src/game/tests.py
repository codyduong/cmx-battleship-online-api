import json
from django.test import TestCase
from django.conf import settings

from app.exceptions import ValidationException, BadRequestException

from game.models import GameBoard, GameState, Play

class GameBoardModelTest(TestCase):

    def test_create_invalid_json_too_many_tiles_for_ship1(self):
        json_str = """{
            "ship_1": ["C1", "C2"]
        }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not hit this code block')
        except ValidationException as e:
            self.assertEqual(e.field, "ship_1", "Should catch invalid value on ship1 of board1")

    def test_create_invalid_json_too_few_tiles_for_ship2(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["F1"]
        }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not hit this code block')
        except ValidationException as e:
            self.assertEqual(e.field, "ship_2", "Should catch invalid value on ship1 of board2")

    def test_create_invalid_json_too_many_tiles_for_ship2(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["F1", "F2", "F3"]
        }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not hit this code block')
        except ValidationException as e:
            self.assertEqual(e.field, "ship_2", "Should catch invalid value on ship1 of board2")

    def test_create_too_many_ships(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["E1", "E2"],
            "ship_3": ["F1", "F2", "F3"],
            "ship_4": ["G1", "G2", "G3", "G4"],
            "ship_5": ["H1", "H2", "H3", "H4", "H5"],
            "ship_6": ["H1", "H2", "H3", "H4", "H5", "H6"]
        }"""

        state = GameBoard(json.loads(json_str))
        for i in range(1, 6):
            self.assertEqual(len(getattr(state, f'ship_{i}')), i, 'each ship should have correct amount of ships')

        self.assertEqual(state.ship_count(), 5, 'should have correct ship count regardless of input')

    def test_create_gameboard_max_ships(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["E1", "E2"],
            "ship_3": ["F1", "F2", "F3"],
            "ship_4": ["G1", "G2", "G3", "G4"],
            "ship_5": ["H1", "H2", "H3", "H4", "H5"]
        }"""

        state = GameBoard(json.loads(json_str))
        for i in range(1, 6):
            self.assertEqual(len(getattr(state, f'ship_{i}')), i, 'each ship should have correct amount of ships')

        self.assertEqual(state.ship_count(), 5, 'should have correct ship count')

    def test_create_gameboard_min_ships(self):
        json_str = """{
            "ship_1": ["C1"]
        }"""

        state = GameBoard(json.loads(json_str))
        for i in range(1, 6):
            if i == 1:
                self.assertEqual(len(getattr(state, f'ship_{i}')), i, 'each ship should have correct amount of ships')
            else:
                self.assertIsNone(getattr(state, f'ship_{i}'))

        self.assertEqual(state.ship_count(), 1, 'should have correct ship count')

    def test_create_invalid_gameboard_min_ships(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_3": ["D1", "D2", "D3"]
        }"""

        state = GameBoard(json.loads(json_str))
        for i in range(1, 6):
            if i == 1:
                self.assertEqual(len(getattr(state, f'ship_{i}')), i, 'each ship should have correct amount of ships')
            else:
                self.assertIsNone(getattr(state, f'ship_{i}'))

        self.assertEqual(state.ship_count(), 1, 'should have correct ship count')

    def test_create_invalid_gameboard_invalid_tiles(self):
        json_str = """{
               "ship_1": ["C1"],
               "ship_2": ["Z2", "C3"],
               "ship_3": ["D1", "E2", "D3"]
           }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not create error state')
        except BadRequestException as e:
            self.assertEqual(e.error, 'invalid column identifier', 'invalid column identifier')

    def test_create_invalid_gameboard_spaced_out_ships(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["C2", "C3"],
            "ship_3": ["D1", "E2", "D3"]
        }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not create error state')
        except ValidationException as e:
            self.assertEqual(e.field, 'ship_3', 'no weird ships allowed')

    def test_create_invalid_gameboard_overlapping_ships(self):
        json_str = """{
            "ship_1": ["C1"],
            "ship_2": ["C1", "C2"],
            "ship_3": ["D1", "D2", "D3"]
        }"""

        try:
            state = GameBoard(json.loads(json_str))
            self.fail('should not create error state')
        except BadRequestException as e:
            self.assertEqual(e.error, 'no overlapping ships', 'no overlapping ships')



class GameStateModelTest(TestCase):
    def test_create_state_from_json(self):
        json = """{
            "p1_attacks": ["A1"],
            "p2_attacks": ["B2"],
            "p1_board": {
                "ship_1": ["C1"]
            },
            "p2_board": {
                "ship_1": ["D1"]
            }
        }"""

        state = GameState(json)
        self.assertEqual(state.p1_attacks[0], 'A1', 'should match json')
        self.assertEqual(state.p1_board.ship_1[0], 'C1', 'should match json')
        response = state.recordPlay('p1', Play({'tile_id':'D1'}))
        self.assertEqual(response.hit_tile_ids, ['D1'], 'D1 was hit')
        self.assertEqual(state.getState('p1').hit_tile_ids, ['D1'], 'D1 was hit')

    def test_get_state(self):
        json = """{
               "p1_attacks": ["A1"],
               "p2_attacks": ["B2"],
               "p1_board": {
                   "ship_1": ["C1"],
                   "ship_2": ["C2", "B2"]
               },
               "p2_board": {
                   "ship_1": ["D1"],
                   "ship_2": ["J2", "J3"]
               }
           }"""

        state = GameState(json)
        response = state.recordPlay('p1',Play({'tile_id':'D1'}))
        self.assertEqual(response.hit_tile_ids, ['D1'], 'D1 was hit')
        self.assertEqual(response.miss_tile_ids, ['A1'], 'A1 was miss')
        self.assertEqual(state.getState('p1').hit_tile_ids, ['D1'], 'D1 was hit')
        self.assertEqual(state.getState('p1').miss_tile_ids, ['A1'], 'A1 was miss')

    def test_state_different_ship_counts(self):
        json = """{
               "p1_attacks": ["A1"],
               "p2_attacks": ["B2"],
               "p1_board": {
                   "ship_1": ["C1"],
                   "ship_2": ["C2", "B2"]
               },
               "p2_board": {
                   "ship_1": ["D1"]
               }
           }"""

        try:
            state = GameState(json)
            self.fail('impossible code')
        except BadRequestException as e:
            self.assertEqual(e.error,
            'players should only be assigned to players with a similar sized board',
            'players should only be assigned to players with a similar sized board')

    def test_delete_this(self):
        json = """{
               "p1_attacks": ["A1"],
               "p2_attacks": ["B2"],
               "p1_board": {
                   "ship_1": ["C1"],
                   "ship_2": ["C2", "B2"]
               },
               "p2_board": {
                   "ship_1": ["D1"],
                   "ship_2": ["J2", "J3"]
               }
           }"""

        state = GameState(json)
        response = state.recordPlay('p1',Play({'tile_id':'D1'}))
        self.assertEqual(response.hit_tile_ids, ['D1'], 'D1 was hit')
        self.assertEqual(response.miss_tile_ids, ['A1'], 'A1 was miss')
        self.assertEqual(state.getState('p1').hit_tile_ids, ['D1'], 'D1 was hit')
        self.assertEqual(state.getState('p1').miss_tile_ids, ['A1'], 'A1 was miss')
        state.json()

