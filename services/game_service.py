"""遊戲流程與商業規則。

這裡回答「玩家做某件事時，系統該怎麼做」，但不印畫面也不直接讀寫 JSON。
"""

from domain.animal import Animal
from domain.animal_rules import (
    ANIMAL_RULES,
    FEED_COST,
    HEALTH_LOSS,
    HEALTH_RECOVERY,
    HUNGER_REDUCTION,
    TOO_HUNGRY,
    VERY_FULL,
)
from domain.zoo_state import ZooState


LAST_DAY = 7


class GameService:
    def __init__(self, repository, scoreboard_repository=None):
        self.repository = repository
        self.scoreboard_repository = scoreboard_repository

    def load_or_create_game(self):
        """先讀存檔；沒有資料時才建立一個新的遊戲。"""
        saved_game = self.repository.load()
        if saved_game is not None:
            return saved_game
        return self.start_new_game()

    def start_new_game(self):
        """建立教學用的預設動物園，並立即存檔。"""
        state = ZooState(
            1,
            20,
            12,
            [
                Animal("Leo", "Lion", hunger=40),
                Animal("Pipi", "Penguin", hunger=25),
                Animal("Momo", "Monkey", hunger=55),
            ],
        )
        self.save_game(state)
        return state

    def save_game(self, state):
        self.repository.save(state)

    def record_final_score(self, state, player_name):
        """把結束遊戲的名字與資金寫入記分板，每局只記錄一次。"""
        if not self.is_finished(state):
            return "遊戲尚未結束，現在不能記錄成績。"
        if state.score_recorded:
            return "這局成績已經記錄過了。"
        if self.scoreboard_repository is None:
            return "記分板目前沒有設定。"

        name = player_name.strip() or "匿名玩家"
        self.scoreboard_repository.add_score(name, state.money)
        state.score_recorded = True
        self.save_game(state)
        return "已記錄 {} 的成績：${}。".format(name, state.money)

    def get_top_scores(self, limit=5):
        """輸出：資金最高的前幾名成績。"""
        if self.scoreboard_repository is None:
            return []
        return self.scoreboard_repository.load_scores()[:limit]

    def feed_animal(self, state, animal_name):
        """餵食流程：找動物 → 檢查規則 → 改狀態 → 存檔 → 回饋。"""
        animal = state.find_animal(animal_name)
        if animal is None:
            return "找不到這隻動物，請確認名字。"
        if state.food < FEED_COST:
            return "食物不足，今天不能再餵食。"
        if animal.hunger <= VERY_FULL:
            return "{} 現在很飽，不需要餵食。".format(animal.name)

        animal.feed(HUNGER_REDUCTION)
        state.food -= FEED_COST
        self.save_game(state)
        return "已餵食 {}：食物 -{}，飢餓度變成 {}。".format(
            animal.name, FEED_COST, animal.hunger
        )

    def end_day(self, state):
        """一天結束：動物變餓、健康改變、園區收入增加、存檔。"""
        income = 0
        for animal in state.animals:
            rule = ANIMAL_RULES[animal.species]
            animal.become_hungrier(rule["hunger_increase"])
            self.apply_health_rule(animal)
            income += self.calculate_income(animal, rule["daily_income"])
        state.money += income
        state.day += 1
        self.save_game(state)
        return "今天結束：收入 ${}，目前資金 ${}。".format(income, state.money)

    def apply_health_rule(self, animal):
        """飢餓太高扣健康；吃得剛好則恢復一些健康。"""
        if animal.hunger >= TOO_HUNGRY:
            animal.change_health(-HEALTH_LOSS)
        elif animal.hunger <= VERY_FULL:
            animal.change_health(HEALTH_RECOVERY)

    @staticmethod
    def calculate_income(animal, base_income):
        """健康越好，動物帶來的收入越接近自己的基本收入。"""
        if animal.health == 0:
            return 0
        return base_income * animal.health // 100

    @staticmethod
    def is_finished(state):
        return state.day > LAST_DAY or any(animal.health == 0 for animal in state.animals)

    @staticmethod
    def get_finish_message(state):
        if any(animal.health == 0 for animal in state.animals):
            return "遊戲結束：有動物的健康降到 0。請從新遊戲再試一次。"
        return "恭喜！你已經成功經營動物園 7 天，最後資金是 ${}。".format(state.money)
