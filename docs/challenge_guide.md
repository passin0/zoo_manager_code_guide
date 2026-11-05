# 挑戰指南

這份指南帶你依序完成三件事：讀懂專案、知道新需求該改哪裡、完成挑戰任務與除錯。

## 1. 先玩，再讀

1. 執行 `python main.py`。
2. 餵食 `Leo`，觀察食物與飢餓度的變化。
3. 結束一天，觀察飢餓度、健康與資金的變化。
4. 離開後再執行一次，確認剛才的進度還在。

看過「操作」之後，再追蹤程式是怎麼完成它的。

## 2. 每個模組負責什麼

| 模組 | 負責 | 不負責 |
| --- | --- | --- |
| `main.py`、`ui/console.py` | 收取選擇、顯示資料和訊息 | 判斷可不可以餵食 |
| `services/game_service.py` | 執行遊戲規則與流程 | 印出畫面、知道 JSON 格式 |
| `domain/` | 保存動物與園區目前的狀態 | 讀取玩家輸入、存檔 |
| `repositories/` | 將狀態保存到檔案、從檔案讀回 | 決定動物會不會餓 |

### 追蹤一次餵食

```text
輸入 Leo
  → main.py 呼叫 game.feed_animal(state, "Leo")
  → GameService 找到 Leo，檢查食物與飢餓度
  → Animal.feed(30) 降低 Leo 的飢餓度
  → GameService.save_game(state) 交給 Repository
  → JsonGameRepository.save(state) 寫入 data/zoo_save.json
  → 回傳「已餵食 Leo...」給畫面顯示
```

### 練習：補完方法表

第一列是示範。請先不要逐行讀程式，只看方法名稱與註解，補完其他列：

| 方法 | 輸入 | 做什麼 | 輸出／效果 |
| --- | --- | --- | --- |
| `Animal.feed(hunger_reduction)` | 要降低的飢餓度 | 降低一隻動物的飢餓度 | 回傳新的飢餓度 |
| `GameService.feed_animal(state, animal_name)` |  |  |  |
| `GameService.end_day(state)` |  |  |  |
| `JsonGameRepository.save(state)` |  |  |  |

## 3. 新需求該改哪裡

| 想做的事 | 優先修改的位置 | 可以使用的現有程式 | 不應該改的位置 |
| --- | --- | --- | --- |
| 新增動物種類 | `domain/animal_rules.py`、`GameService.start_new_game()` | `ANIMAL_RULES`、`Animal(name, species, ...)` | 不需要新增類別或修改存檔格式 |
| 修改餵食效果 | `domain/animal_rules.py`、`GameService.feed_animal()` | `FEED_COST`、`HUNGER_REDUCTION`、`Animal.feed()` | UI 不判斷規則 |
| 新增每日規則 | `GameService.end_day()`、`apply_health_rule()` | `Animal.become_hungrier()`、`Animal.change_health()` | Repository 不決定規則 |
| 新增玩家操作 | 在 `GameService` 新增方法，再從 `main.py` 呼叫 | `GameService` 回傳的訊息字串 | `main.py` 不直接修改動物資料 |
| 更換保存方式 | 新增另一個 Repository 類別 | `load()`、`save(state)` | `GameService` 不需要知道檔案格式 |
| 新增顯示資訊 | `ui/console.py` | `show_game_state(state)` | 不把規則寫進 UI |

### 模組之間的約定

- **`Animal`**：`feed()`、`become_hungrier()`、`change_health()` 只更新一隻動物，並回傳新的數值；不存檔、不印訊息。
- **`GameService`**：每個玩家操作都依照「接收狀態與輸入 → 檢查規則 → 更新狀態 → `save_game(state)` → 回傳訊息」的順序。
- **Repository**：遊戲存檔只需要 `load()`（回傳 `ZooState` 或 `None`）與 `save(state)`；記分板只需要 `add_score(name, money)` 與 `load_scores()`。兩者分別存在 `data/zoo_save.json` 與 `data/scoreboard.json`，因為一個會持續更新、一個只在遊戲結束時新增一筆。

## 4. 修改的工作流程

每個挑戰都照這個順序進行：

1. 複製 [`templates/feature_change_plan.md`](../templates/feature_change_plan.md)，自己先填完。
2. 把變更單交給 AI，要求它**先不要修改程式**，只提出最小修改計畫。
3. 確認計畫合理後才讓 AI 實作。
4. 依變更單的驗收表補測試（可以從 [`templates/new_rule_test.py.example`](../templates/new_rule_test.py.example) 開始），並跑完全部測試。

## 5. 挑戰任務

### Level 1：增加顯示資訊

目標：在畫面上顯示每種動物「一天會增加多少飢餓度」。

想一想：規則存在哪個檔案？顯示又在哪個檔案？

### Level 2：新增規則

目標：動物健康低於 40 時，餵食一次額外恢復 5 點健康。

想一想：何時觸發？改變哪個狀態？畫面要回饋什麼？要新增哪些測試？

### Level 3：新增動物

目標：自己設計一種新動物，決定牠的名字、每日飢餓度與基本收入，加進預設的動物園。

可以使用 [`templates/new_animal.md`](../templates/new_animal.md)。完成後跑一次全部測試，並解釋哪些測試失敗了、為什麼。

### Level 4：新增玩家操作

目標：加入「購買食物」或「治療動物」等新選項。

可以使用 [`templates/new_action.md`](../templates/new_action.md)。

## 6. 除錯練習

### 思考題：資料沒有存下來

假設你看到「已餵食」，但關掉再開遊戲後，飢餓度又變回原本的數字。你會沿著這條路檢查：

```text
回饋訊息有出現？
  → GameService 是否真的呼叫 save_game？
  → Repository 是否真的寫入檔案？
  → 讀檔時是否把 JSON 正確還原成 ZooState？
```

發現問題的位置，不一定是真正壞掉的位置。

### 實戰：找出專案裡的 Bug

這個專案裡預留了一個 bug。請和 AI 一起：

1. 重現：完整玩完一局，再重新啟動遊戲，結果符合你的預期嗎？
2. 描述：哪個操作之後、看到了什麼、預期應該是什麼？
3. 分析：請 AI 先說明可能原因與證據，再提出最小修正方案；確認後才修改。
4. 驗證：修正後重跑測試，並想想為什麼現有測試沒有抓到它。
