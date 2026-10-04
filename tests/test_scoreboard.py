import tempfile
import unittest
from pathlib import Path

from repositories.json_scoreboard_repository import JsonScoreboardRepository
from services.game_service import GameService


class MemoryRepository:
    def save(self, state):
        self.saved_state = state

    def load(self):
        return None


class ScoreboardTests(unittest.TestCase):
    def test_scores_are_saved_sorted_and_limited_to_top_five_when_read(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            score_file = Path(temporary_folder) / "scoreboard.json"
            scoreboard = JsonScoreboardRepository(score_file)
            for name, money in [("A", 20), ("B", 80), ("C", 50), ("D", 70), ("E", 60), ("F", 40)]:
                scoreboard.add_score(name, money)

            top_five = scoreboard.load_scores()[:5]

        self.assertEqual([score["name"] for score in top_five], ["B", "D", "E", "C", "F"])

    def test_finished_game_records_one_final_score_only(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            scoreboard = JsonScoreboardRepository(Path(temporary_folder) / "scoreboard.json")
            game = GameService(MemoryRepository(), scoreboard)
            state = game.start_new_game()
            state.day = 8

            first_result = game.record_final_score(state, "Ada")
            second_result = game.record_final_score(state, "Ada")

            self.assertIn("已記錄 Ada", first_result)
            self.assertIn("已經記錄過", second_result)
            self.assertEqual(scoreboard.load_scores(), [{"name": "Ada", "money": 20}])
