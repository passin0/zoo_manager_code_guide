import unittest

from animals.animal import Animal
from animals.elephant import Elephant
from animals.lion import Lion
from animals.penguin import Penguin
from feeding.feeder import feed_one_animal


class AnimalTests(unittest.TestCase):
    def test_animal_keeps_its_name(self):
        animal = Animal("小動物")

        self.assertEqual(animal.name, "小動物")
        self.assertEqual(animal.speak(), "動物發出聲音。")

    def test_lion_inherits_animal_and_has_its_own_sound(self):
        lion = Lion("Leo")

        self.assertIsInstance(lion, Animal)
        self.assertEqual(lion.name, "Leo")
        self.assertEqual(lion.speak(), "吼！")

    def test_elephant_inherits_animal_and_has_its_own_sound(self):
        elephant = Elephant("Eli")

        self.assertIsInstance(elephant, Animal)
        self.assertEqual(elephant.name, "Eli")
        self.assertEqual(elephant.speak(), "哞！")

    def test_penguin_inherits_animal_and_has_its_own_sound(self):
        penguin = Penguin("Penny")

        self.assertIsInstance(penguin, Animal)
        self.assertEqual(penguin.name, "Penny")
        self.assertEqual(penguin.speak(), "嘎！")

    def test_animals_have_different_food_and_hunger_speeds(self):
        lion = Lion("Leo")
        elephant = Elephant("Ella")
        penguin = Penguin("Penny")

        self.assertEqual(lion.food_type, "肉")
        self.assertEqual(elephant.food_type, "草")
        self.assertEqual(penguin.food_type, "肉")
        self.assertEqual(lion.hunger_increase_per_day, 20)
        self.assertEqual(elephant.hunger_increase_per_day, 10)
        self.assertEqual(penguin.hunger_increase_per_day, 15)

    def test_hunger_increases_at_the_start_of_each_day(self):
        lion = Lion("Leo", hunger=20)
        elephant = Elephant("Ella", hunger=20)

        lion.start_day()
        elephant.start_day()

        self.assertEqual(lion.hunger, 40)
        self.assertEqual(elephant.hunger, 30)

    def test_hunger_does_not_go_above_100(self):
        lion = Lion("Leo", hunger=95)

        lion.start_day()

        self.assertEqual(lion.hunger, 100)

    def test_initial_hunger_and_health_stay_between_zero_and_100(self):
        lion = Lion("Leo", hunger=-10, health=120)

        self.assertEqual(lion.hunger, 0)
        self.assertEqual(lion.health, 100)

    def test_negative_hunger_increase_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Animal("小動物", hunger_increase_per_day=-1)

    def test_animal_only_eats_its_correct_food(self):
        lion = Lion("Leo", hunger=70)

        self.assertFalse(lion.eat("草"))
        self.assertEqual(lion.hunger, 70)

        self.assertTrue(lion.eat("肉"))
        self.assertEqual(lion.hunger, 30)

    def test_animal_that_is_not_hungry_does_not_eat(self):
        elephant = Elephant("Ella", hunger=0)

        elephant.eat("草")

        self.assertEqual(elephant.hunger, 0)

    def test_feeding_costs_stock_and_reduces_hunger(self):
        lion = Lion("Leo", hunger=70)

        was_fed, remaining_feed = feed_one_animal(lion, 10)

        self.assertTrue(was_fed)
        self.assertEqual(remaining_feed, 8)
        self.assertEqual(lion.hunger, 30)

    def test_cannot_feed_without_enough_stock(self):
        lion = Lion("Leo", hunger=70)

        was_fed, remaining_feed = feed_one_animal(lion, 1)

        self.assertFalse(was_fed)
        self.assertEqual(remaining_feed, 1)
        self.assertEqual(lion.hunger, 70)

    def test_health_changes_at_the_end_of_the_day(self):
        hungry_lion = Lion("Leo", hunger=80, health=85)
        well_fed_penguin = Penguin("Pipi", hunger=20, health=85)

        hungry_lion.finish_day()
        well_fed_penguin.finish_day()

        self.assertEqual(hungry_lion.health, 75)
        self.assertEqual(well_fed_penguin.health, 87)


if __name__ == "__main__":
    unittest.main()
