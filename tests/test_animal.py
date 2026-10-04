import unittest

from domain.animal import Animal


class AnimalTests(unittest.TestCase):
    def test_feed_reduces_hunger_but_not_below_zero(self):
        leo = Animal("Leo", "Lion", hunger=20)

        hunger_after_feeding = leo.feed(30)

        self.assertEqual(hunger_after_feeding, 0)
        self.assertEqual(leo.hunger, 0)

    def test_health_stays_between_zero_and_one_hundred(self):
        pipi = Animal("Pipi", "Penguin", health=95)

        pipi.change_health(10)

        self.assertEqual(pipi.health, 100)
