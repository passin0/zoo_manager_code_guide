"""用 JSON 檔長期保存所有已完成遊戲的分數。"""

import json
from pathlib import Path

from repositories.scoreboard_repository import ScoreboardRepository


class JsonScoreboardRepository(ScoreboardRepository):
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load_scores(self):
        """輸出：依資金由高到低排列的所有成績。"""
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as score_file:
            scores = json.load(score_file)
        return sorted(scores, key=lambda score: score["money"], reverse=True)

    def add_score(self, name, money):
        """輸入：玩家名稱與最終資金。效果：新增一筆長期成績。"""
        scores = self.load_scores()
        scores.append({"name": name, "money": money})
        scores = sorted(scores, key=lambda score: score["money"], reverse=True)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as score_file:
            json.dump(scores, score_file, ensure_ascii=False, indent=2)

        return scores
