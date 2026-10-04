# 擴充指南：新需求應該放在哪裡？

這份指南是給學生與 AI 的「專案地圖」。先找到需求屬於哪一種，再做最小修改；不要因為找到一個熟悉的檔案，就把所有程式塞進去。

## 可使用的擴充介面

| 想做的事 | 優先使用的位置 | 已有的介面／資料 | 不應修改的位置 |
| --- | --- | --- | --- |
| 新增動物種類 | `domain/animal_rules.py`、`GameService.start_new_game()` | `ANIMAL_RULES`、`Animal(name, species, ...)` | 不需要新增繼承類別或改 JSON 存檔 |
| 修改餵食效果 | `domain/animal_rules.py`、`GameService.feed_animal()` | `FEED_COST`、`HUNGER_REDUCTION`、`Animal.feed()` | `ui/console.py` 不判斷規則 |
| 新增每日規則 | `GameService.end_day()` 或 `apply_health_rule()` | `Animal.become_hungrier()`、`Animal.change_health()` | Repository 不決定規則 |
| 新增玩家操作 | `GameService` 新增一個方法，再從 `main.py` 呼叫 | Service 回傳給玩家的文字訊息 | `main.py` 不直接改動 Animal 的資料 |
| 更換保存方式 | 新增另一個 Repository | `GameRepository.load()`、`GameRepository.save(state)` | `GameService` 不應知道檔案格式 |
| 記錄完成成績 | `ScoreboardRepository` | `add_score(name, money)`、`load_scores()` | 不要把所有歷史成績塞進單一遊戲存檔 |
| 新增顯示資訊 | `ui/console.py` | `show_game_state(state)` | 不把新規則寫進 UI |

## 目前的模組合約

### `Animal`

`Animal` 只管理一隻動物本身的資料與狀態。

```python
animal.feed(hunger_reduction)
animal.become_hungrier(hunger_increase)
animal.change_health(amount)
```

這些方法會更新 Animal，並回傳更新後的數字。它們不存檔、不印訊息、不知道玩家按了什麼。

### `GameService`

`GameService` 是玩家操作的入口。新增操作時，請讓它：

1. 接收 `state` 與需要的輸入；
2. 檢查規則與例外；
3. 更新 Domain 資料；
4. 呼叫 `save_game(state)`；
5. 回傳人看得懂的結果訊息。

例如：

```python
result = game.feed_animal(state, "Leo")
```

UI 不必理解餵食的細節，只要顯示 `result`。

### `GameRepository`

存檔工具只需要承諾兩件事：

```python
repository.load()       # 回傳 ZooState 或 None
repository.save(state)  # 保存 ZooState
```

若未來改成 SQLite，新增 `SqliteGameRepository` 即可；遊戲規則與 UI 不需要一起重寫。

### `ScoreboardRepository`

記分板是第二個長期保存範例。它不保存一局遊戲的所有動物，而是只保存已結束遊戲的結果：

```python
scoreboard.add_score(name, money)
scoreboard.load_scores()
```

這份資料存於 `data/scoreboard.json`；它和 `data/zoo_save.json` 分開，讓學生觀察不同資料有不同保存責任。

## 擴充工作流程

複製 `templates/feature_change_plan.md`，先填完再請 AI 規劃。完成後至少要有：

- 一個新功能的一般情況測試；
- 一個例外情況測試；
- 一次既有功能的回歸測試。

可直接使用 `templates/new_rule_test.py.example` 作為測試起點。
