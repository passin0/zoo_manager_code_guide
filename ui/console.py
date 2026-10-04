"""純文字介面。它只顯示資料與結果，不決定遊戲規則。"""


def show_game_state(state):
    print("\n=== 第 {} 天 ===".format(state.day))
    print("資金：${}　食物：{}".format(state.money, state.food))
    print("\n動物：")
    for animal in state.animals:
        print("- {}（{}）｜飢餓：{}｜健康：{}".format(animal.name, animal.species, animal.hunger, animal.health))


def show_help():
    print("\n1. 餵食動物")
    print("2. 結束今天")
    print("3. 重新開始")
    print("0. 儲存並離開")


def show_action_result(message):
    print("\n→ {}".format(message))


def show_leaderboard(scores):
    """顯示資金最高的前五名，不負責計算或排序。"""
    print("\n=== 記分板：前五名 ===")
    if not scores:
        print("目前還沒有成績。")
        return

    for position, score in enumerate(scores, start=1):
        print("{}. {}　${}".format(position, score["name"], score["money"]))
