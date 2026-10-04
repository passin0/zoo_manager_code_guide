# 新增動物模板

## 設計資料

| 欄位 | 填寫內容 |
| --- | --- |
| 種類名稱（英文） | `Rabbit` |
| 顯示名字 | `Bunny` |
| 每日增加飢餓 | `12` |
| 健康 100 時的每日收入 | `4` |

## 最小修改位置

1. 在 `domain/animal_rules.py` 的 `ANIMAL_RULES` 加入一筆規則：

```python
"Rabbit": {"hunger_increase": 12, "daily_income": 4},
```

2. 在 `services/game_service.py` 的 `start_new_game()` 加入初始動物：

```python
Animal("Bunny", "Rabbit", hunger=35),
```

3. 在 `tests/test_game_service.py` 增加測試，確認結束一天後 Rabbit 的飢餓度依規則增加。

## 不需要修改

- 不需要建立 `rabbit.py`。
- 不需要修改 JSON Repository。
- 不需要在 `main.py` 加特殊判斷；畫面會自動顯示新動物。
