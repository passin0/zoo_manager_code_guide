import unittest

from domain.animal import Animal
from domain.zoo_state import ZooState
from services.game_service import GameService


class MemoryRepository:
    """測試專用的假存檔工具，不會建立真正的檔案。"""

    def __init__(self):
        self.saved_state = None

    def load(self):
        return self.saved_state

    def save(self, state):
        self.saved_state = state


class GameServiceTests(unittest.TestCase):
    def setUp(self):
        self.repository = MemoryRepository()
        self.game = GameService(self.repository)
        self.state = self.game.start_new_game()

    def test_feeding_uses_food_reduces_hunger_and_saves(self):
        result = self.game.feed_animal(self.state, "Leo")

        self.assertIn("已餵食 Leo", result)
        self.assertEqual(self.state.food, 11)
        self.assertEqual(self.state.find_animal("Leo").hunger, 10)
        self.assertIs(self.repository.saved_state, self.state)

    def test_cannot_feed_an_animal_that_is_already_full(self):
        result = self.game.feed_animal(self.state, "Pipi")

        self.assertIn("不需要餵食", result)
        self.assertEqual(self.state.food, 12)

    def test_end_day_makes_animals_hungrier_and_earns_income(self):
        result = self.game.end_day(self.state)

        self.assertIn("收入 $19", result)
        self.assertEqual(self.state.day, 2)
        self.assertEqual(self.state.money, 39)
        self.assertEqual(self.state.find_animal("Leo").hunger, 65)
        self.assertEqual(self.state.find_animal("Pipi").hunger, 40)
        self.assertEqual(self.state.find_animal("Momo").hunger, 75)

    def test_too_hungry_animal_loses_health_at_end_of_day(self):
        state = ZooState(1, 20, 12, [Animal("Leo", "Lion", hunger=70)])

        self.game.end_day(state)

        self.assertEqual(state.animals[0].hunger, 95)
        self.assertEqual(state.animals[0].health, 85)

    def test_game_finishes_when_an_animal_has_no_health(self):
        state = ZooState(1, 20, 12, [Animal("Leo", "Lion", health=0)])

        self.assertTrue(self.game.is_finished(state))
        self.assertIn("健康降到 0", self.game.get_finish_message(state))
