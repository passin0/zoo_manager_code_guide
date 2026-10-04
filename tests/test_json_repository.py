import tempfile
import unittest
from pathlib import Path

from repositories.json_game_repository import JsonGameRepository
from services.game_service import GameService


class JsonGameRepositoryTests(unittest.TestCase):
    def test_save_then_load_keeps_the_same_game_state(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            save_file = Path(temporary_folder) / "zoo_save.json"
            repository = JsonGameRepository(save_file)
            game = GameService(repository)
            state = game.start_new_game()
            game.feed_animal(state, "Leo")

            loaded_state = repository.load()

        self.assertEqual(loaded_state.day, 1)
        self.assertEqual(loaded_state.food, 11)
        self.assertEqual(loaded_state.find_animal("Leo").hunger, 10)
