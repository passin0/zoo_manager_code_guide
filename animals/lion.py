"""獅子類別。"""

from animals.animal import Animal


class Lion(Animal):
    def __init__(self, name, hunger=0, health=85):
        super().__init__(
            name,
            food_type="肉",
            hunger_increase_per_day=20,
            hunger=hunger,
            health=health,
        )

    def speak(self):
        return "吼！"
