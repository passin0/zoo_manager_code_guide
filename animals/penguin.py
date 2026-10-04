"""企鵝類別。"""

from animals.animal import Animal


class Penguin(Animal):
    def __init__(self, name, hunger=0, health=85):
        super().__init__(
            name,
            food_type="肉",
            hunger_increase_per_day=15,
            hunger=hunger,
            health=health,
        )

    def speak(self):
        return "嘎！"
