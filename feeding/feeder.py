"""玩家餵食動物時的規則。"""

from feeding.food import FEED_COST


def feed_one_animal(animal, feed_stock):
    """嘗試餵一隻動物，回傳是否成功和剩餘飼料。"""
    if feed_stock < FEED_COST:
        return False, feed_stock

    if not animal.eat(animal.food_type):
        return False, feed_stock

    return True, feed_stock - FEED_COST
