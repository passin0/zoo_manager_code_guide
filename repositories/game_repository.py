"""遊戲存檔介面。

GameService 只要求存檔工具有 load 與 save；它不需要知道資料放在 JSON、
資料庫或雲端。這就是模組之間的 Interface。
"""


class GameRepository:
    def load(self):
        raise NotImplementedError

    def save(self, state):
        raise NotImplementedError
