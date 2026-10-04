"""Animal：一隻動物本身知道的資料與狀態。"""


class Animal:
    """不處理存檔或畫面，只保存一隻動物目前的狀態。"""

    def __init__(self, name, species, hunger=0, health=100):
        self.name = name
        self.species = species
        self.hunger = self.keep_in_range(hunger)
        self.health = self.keep_in_range(health)

    def feed(self, hunger_reduction):
        """輸入：降低多少飢餓。輸出：餵食後的飢餓度。"""
        self.hunger = self.keep_in_range(self.hunger - hunger_reduction)
        return self.hunger

    def become_hungrier(self, hunger_increase):
        """輸入：一天增加的飢餓。輸出：更新後的飢餓度。"""
        self.hunger = self.keep_in_range(self.hunger + hunger_increase)
        return self.hunger

    def change_health(self, amount):
        """輸入：健康要增加或減少的數字。輸出：更新後的健康。"""
        self.health = self.keep_in_range(self.health + amount)
        return self.health

    def to_dict(self):
        """把物件轉成可存進 JSON 檔案的普通資料。"""
        return {"name": self.name, "species": self.species, "hunger": self.hunger, "health": self.health}

    @staticmethod
    def keep_in_range(value):
        """讓健康與飢餓永遠維持在 0 到 100。"""
        return max(0, min(100, value))
