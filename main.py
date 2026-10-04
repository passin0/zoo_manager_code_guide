"""A small zoo feeding program for Python beginners."""

from animals.elephant import Elephant
from animals.lion import Lion
from animals.penguin import Penguin
from feeding.feeder import feed_one_animal
from feeding.food import FEED_COST


def find_animal(name, animals):
    """Find an animal by name. Return None if it is not in the list."""
    for animal in animals:
        if animal["name"] == name:
            return animal
    return None


def feed_animal(name, animals):
    """餵食字典中的動物，保留給初學者練習函式和字典。"""
    animal = find_animal(name, animals)

    if animal is None:
        return "找不到這隻動物。"

    if animal["hunger"] <= 30:
        return "這隻動物已經吃飽了。"

    animal["hunger"] = animal["hunger"] - 60

    if animal["hunger"] < 0:
        animal["hunger"] = 0

    return "餵食成功。"


class ZooGame:
    def __init__(self):
        self.animals = [
            Lion("Leo", hunger=55),
            Penguin("Pipi", hunger=10),
        ]
        self.feed_stock = 20
        self.money = 0
        self.day = 1
        self.day_started = False
        self.fed_today = []

    @property
    def zoo_health(self):
        total_health = 0
        for animal in self.animals:
            total_health = total_health + animal.health
        return total_health // len(self.animals)

    def start_day(self):
        if self.day_started:
            return

        for animal in self.animals:
            animal.start_day()
        self.fed_today = []
        self.day_started = True

    def feed(self, animal_name):
        if not self.day_started:
            raise RuntimeError("請先開始今天，再餵食動物。")

        animal = None
        for current_animal in self.animals:
            if current_animal.name == animal_name:
                animal = current_animal
                break

        if animal is None:
            return "找不到這隻動物。"

        if animal.name in self.fed_today:
            return "{} 今天已經餵過了。".format(animal.name)

        was_fed, remaining_feed = feed_one_animal(animal, self.feed_stock)
        if not was_fed:
            if self.feed_stock < FEED_COST:
                return "飼料不夠了。"
            return "{} 現在不需要吃東西。".format(animal.name)

        self.feed_stock = remaining_feed
        self.fed_today.append(animal.name)
        return "{} 吃了{}，消耗 {} 份飼料。".format(
            animal.name, animal.food_type, FEED_COST
        )

    def finish_day(self):
        if not self.day_started:
            raise RuntimeError("今天還沒有開始。")

        for animal in self.animals:
            animal.finish_day()

        daily_income = 5
        self.money = self.money + daily_income
        report = {
            "day": self.day,
            "animals": [
                {
                    "name": animal.name,
                    "hunger": animal.hunger,
                    "health": animal.health,
                }
                for animal in self.animals
            ],
            "feed_stock": self.feed_stock,
            "daily_income": daily_income,
            "money": self.money,
            "zoo_health": self.zoo_health,
        }
        self.day = self.day + 1
        self.day_started = False
        return report


def show_zoo(game):
    print("\n我的動物園 - Day {}".format(game.day))
    print("--------------------")
    for index, animal in enumerate(game.animals, start=1):
        filled_blocks = animal.hunger * 8 // 100
        hunger_bar = "#" * filled_blocks + "-" * (8 - filled_blocks)
        print("{} {}".format(animal.name, animal.speak()))
        print("  飢餓度：{} {}".format(hunger_bar, animal.hunger))
        print("  健康：{}".format(animal.health))

    print("--------------------")
    print("飼料：{}".format(game.feed_stock))
    print("動物園健康：{}".format(game.zoo_health))
    print("累計收益：${}".format(game.money))


def show_day_report(report):
    print("\nDay {}".format(report["day"]))
    for animal in report["animals"]:
        print("{}    健康 {}    飢餓度 {}".format(
            animal["name"], animal["health"], animal["hunger"]
        ))
    print("飼料剩餘：{}".format(report["feed_stock"]))
    print("今日收益：+${}".format(report["daily_income"]))
    print("累計收益：${}".format(report["money"]))
    print("動物園健康：{}".format(report["zoo_health"]))


def main():
    game = ZooGame()

    print("歡迎來到「養活你的動物園」！")
    print("每天餵食一次會消耗 {} 份飼料。".format(FEED_COST))
    print("飢餓度越高越餓；每天結束時，太餓會影響健康。")

    while True:
        game.start_day()
        show_zoo(game)

        for index, animal in enumerate(game.animals, start=1):
            print("{}. 餵食 {}".format(index, animal.name))
        print("{}. 結束今天".format(len(game.animals) + 1))
        print("0. 離開遊戲")

        choice = input("請選擇：").strip()
        if choice == "0":
            print("遊戲結束。")
            break

        if choice == str(len(game.animals) + 1):
            show_day_report(game.finish_day())
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(game.animals):
            animal = game.animals[int(choice) - 1]
            print(game.feed(animal.name))
            continue

        print("輸入無效，請選擇清單上的數字。")


if __name__ == "__main__":
    main()
