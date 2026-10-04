"""ZooState：一座動物園需要記住的整體狀態。"""

from domain.animal import Animal


class ZooState:
    def __init__(self, day, money, food, animals, score_recorded=False):
        self.day = day
        self.money = money
        self.food = food
        self.animals = animals
        self.score_recorded = score_recorded

    def find_animal(self, name):
        """輸入：動物名字。輸出：找到的 Animal，或 None。"""
        for animal in self.animals:
            if animal.name.lower() == name.lower():
                return animal
        return None

    def to_dict(self):
        return {
            "day": self.day,
            "money": self.money,
            "food": self.food,
            "animals": [animal.to_dict() for animal in self.animals],
            "score_recorded": self.score_recorded,
        }

    @classmethod
    def from_dict(cls, data):
        animals = [Animal(item["name"], item["species"], item["hunger"], item["health"]) for item in data["animals"]]
        return cls(
            data["day"],
            data["money"],
            data["food"],
            animals,
            data.get("score_recorded", False),
        )
