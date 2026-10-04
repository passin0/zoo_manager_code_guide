import unittest

from main import feed_animal, find_animal


class ZooProgramTests(unittest.TestCase):
    def setUp(self):
        self.animals = [
            {"name": "Leo", "species": "Lion", "hunger": 80},
            {"name": "Mia", "species": "Cat", "hunger": 20},
        ]

    def test_find_animal(self):
        animal = find_animal("Leo", self.animals)

        self.assertEqual(animal["species"], "Lion")

    def test_find_missing_animal(self):
        animal = find_animal("Unknown", self.animals)

        self.assertIsNone(animal)

    def test_feed_animal(self):
        message = feed_animal("Leo", self.animals)

        self.assertEqual(message, "餵食成功。")
        self.assertEqual(self.animals[0]["hunger"], 20)

    def test_feed_animal_that_is_already_full(self):
        message = feed_animal("Mia", self.animals)

        self.assertEqual(message, "這隻動物已經吃飽了。")
        self.assertEqual(self.animals[1]["hunger"], 20)

    def test_feed_animal_that_does_not_exist(self):
        message = feed_animal("Unknown", self.animals)

        self.assertEqual(message, "找不到這隻動物。")

    def test_feeding_does_not_make_hunger_negative(self):
        animals = [{"name": "Mia", "species": "Cat", "hunger": 31}]

        feed_animal("Mia", animals)

        self.assertEqual(animals[0]["hunger"], 0)


if __name__ == "__main__":
    unittest.main()
