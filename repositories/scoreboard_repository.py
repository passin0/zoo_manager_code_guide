"""記分板存檔介面。

它和 GameRepository 分開，因為兩者保存的資料與生命週期不同：
遊戲存檔會被同一位玩家持續更新；記分板只在遊戲結束時新增一筆成績。
"""


class ScoreboardRepository:
    def load_scores(self):
        raise NotImplementedError

    def add_score(self, name, money):
        raise NotImplementedError
