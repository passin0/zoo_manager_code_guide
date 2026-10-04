"""動物園遊戲的程式入口。

這個檔案只負責把使用者操作交給遊戲服務，再把結果顯示出來。
遊戲規則不寫在這裡，這樣日後改規則時不會同時弄壞畫面。
"""

from repositories.json_game_repository import JsonGameRepository
from repositories.json_scoreboard_repository import JsonScoreboardRepository
from services.game_service import GameService
from ui.console import show_action_result, show_game_state, show_help, show_leaderboard


SAVE_FILE = "data/zoo_save.json"
SCOREBOARD_FILE = "data/scoreboard.json"


def create_game():
    """建立服務需要的存檔工具，並交給它管理遊戲。"""
    repository = JsonGameRepository(SAVE_FILE)
    scoreboard_repository = JsonScoreboardRepository(SCOREBOARD_FILE)
    return GameService(repository, scoreboard_repository)


def main():
    game = create_game()
    state = game.load_or_create_game()

    print("歡迎來到小小動物園！")
    print("目標：照顧動物園到第 7 天，別讓任何動物的健康降到 0。")

    while True:
        show_game_state(state)

        if game.is_finished(state):
            show_action_result(game.get_finish_message(state))
            if not state.score_recorded:
                player_name = input("請輸入你的名字，記錄最後資金：")
                show_action_result(game.record_final_score(state, player_name))
            show_leaderboard(game.get_top_scores())
            break

        show_help()
        choice = input("請選擇：").strip()

        if choice == "1":
            name = input("要餵哪一隻動物？").strip()
            result = game.feed_animal(state, name)
        elif choice == "2":
            result = game.end_day(state)
        elif choice == "3":
            state = game.start_new_game()
            result = "已建立新的動物園。"
        elif choice == "0":
            game.save_game(state)
            print("遊戲已存檔，再見！")
            break
        else:
            result = "請輸入選單上的數字。"

        show_action_result(result)


if __name__ == "__main__":
    main()
