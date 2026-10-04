"""所有動物都會共用的基本設定。"""

from feeding.food import HUNGER_REDUCTION


class Animal:
    def __init__(self, name, food_type=None, hunger_increase_per_day=10, hunger=0, health=85):
        if hunger_increase_per_day < 0:
            raise ValueError("每日飢餓增加量不能是負數。")

        self.name = name
        self.food_type = food_type
        self.hunger_increase_per_day = hunger_increase_per_day
        self.hunger = self._keep_in_range(hunger)
        self.health = self._keep_in_range(health)

    def speak(self):
        return "動物發出聲音。"

    def start_day(self):
        self.hunger = self._keep_in_range(
            self.hunger + self.hunger_increase_per_day
        )

    def eat(self, food_type):
        if self.food_type is None or food_type != self.food_type or self.hunger == 0:
            return False

        self.hunger = self._keep_in_range(self.hunger - HUNGER_REDUCTION)
        return True

    def finish_day(self):
        if self.hunger >= 70:
            self.health = self._keep_in_range(self.health - 10)
        elif self.hunger <= 30:
            self.health = self._keep_in_range(self.health + 2)

    @staticmethod
    def _keep_in_range(value):
        if value < 0:
            return 0
        if value > 100:
            return 100
        return value
