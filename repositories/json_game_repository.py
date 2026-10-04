"""用一個本機 JSON 檔案保存遊戲。"""

import json
from pathlib import Path

from domain.zoo_state import ZooState
from repositories.game_repository import GameRepository


class JsonGameRepository(GameRepository):
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load(self):
        """輸出：已保存的 ZooState；沒有存檔時輸出 None。"""
        if not self.file_path.exists():
            return None
        with self.file_path.open("r", encoding="utf-8") as save_file:
            return ZooState.from_dict(json.load(save_file))

    def save(self, state):
        """輸入：ZooState。效果：將目前狀態寫進 JSON 檔。"""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as save_file:
            json.dump(state.to_dict(), save_file, ensure_ascii=False, indent=2)
