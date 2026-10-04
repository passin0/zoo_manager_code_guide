"""不同動物的差異資料。

新增一種動物時，先在這裡加入規則。
"""

ANIMAL_RULES = {
    "Lion": {"hunger_increase": 25, "daily_income": 8},
    "Penguin": {"hunger_increase": 15, "daily_income": 6},
    "Monkey": {"hunger_increase": 20, "daily_income": 5},
}

FEED_COST = 1
HUNGER_REDUCTION = 30
TOO_HUNGRY = 80
VERY_FULL = 30
HEALTH_LOSS = 15
HEALTH_RECOVERY = 5
