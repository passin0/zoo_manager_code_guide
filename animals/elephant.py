"""大象類別。"""

from animals.animal import Animal


class Elephant(Animal):
    def __init__(self, name, hunger=0, health=85):
        super().__init__(
            name,
            food_type="草",
            hunger_increase_per_day=10,
            hunger=hunger,
            health=health,
        )

    def speak(self):
        return "哞！"
