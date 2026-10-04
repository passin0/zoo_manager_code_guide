import unittest

from main import ZooGame


class ZooGameTests(unittest.TestCase):
    def setUp(self):
        self.game = ZooGame()

    def test_starting_day_increases_each_animal_hunger(self):
        self.game.start_day()

        self.assertEqual(self.game.animals[0].hunger, 75)
        self.assertEqual(self.game.animals[1].hunger, 25)

    def test_feeding_uses_stock_and_reduces_hunger(self):
        self.game.start_day()

        message = self.game.feed("Leo")

        self.assertIn("吃了肉", message)
        self.assertEqual(self.game.feed_stock, 18)
        self.assertEqual(self.game.animals[0].hunger, 35)

    def test_each_animal_can_only_be_fed_once_per_day(self):
        self.game.start_day()
        self.game.feed("Leo")

        message = self.game.feed("Leo")

        self.assertEqual(message, "Leo 今天已經餵過了。")
        self.assertEqual(self.game.feed_stock, 18)
        self.assertEqual(self.game.animals[0].hunger, 35)

    def test_feeding_unknown_animal_does_not_change_stock(self):
        self.game.start_day()

        message = self.game.feed("Unknown")

        self.assertEqual(message, "找不到這隻動物。")
        self.assertEqual(self.game.feed_stock, 20)

    def test_ending_day_updates_health_income_and_day_number(self):
        self.game.start_day()
        self.game.feed("Leo")

        report = self.game.finish_day()

        self.assertEqual(report["day"], 1)
        self.assertEqual(report["animals"][0]["health"], 85)
        self.assertEqual(report["animals"][1]["health"], 87)
        self.assertEqual(report["daily_income"], 5)
        self.assertEqual(report["money"], 5)
        self.assertEqual(report["feed_stock"], 18)
        self.assertEqual(self.game.day, 2)
        self.assertFalse(self.game.day_started)

    def test_unfed_hungry_animal_loses_health_at_day_end(self):
        self.game.start_day()

        report = self.game.finish_day()

        self.assertEqual(report["animals"][0]["health"], 75)


if __name__ == "__main__":
    unittest.main()
