# Zoo 範例：用教材觀念讀一個小專案

這個專案不是要你先學完 Python。請先把它當成一座小工廠：每個檔案負責一件事，彼此交接資料。

## 先玩，再讀

1. 執行 `python main.py`。
2. 餵食 `Leo`，觀察食物與飢餓度改變。
3. 結束一天，觀察動物變餓、健康與資金的改變。
4. 離開後再執行一次，確認剛才的結果還在。

現在你已經看過「操作」；接下來才追蹤程式如何完成它。

## 模組地圖

```text
玩家輸入
  ↓
main.py + ui/console.py      顯示畫面、收取選擇
  ↓
services/game_service.py     餵食、結束一天、判斷遊戲是否結束
  ↓                 ↓
domain/                 repositories/
動物與園區狀態          JSON 存檔的讀取與保存
```

| 模組 | 主要責任 | 不負責什麼 |
| --- | --- | --- |
| `ui/console.py` | 顯示資料和訊息 | 決定可不可以餵食 |
| `services/game_service.py` | 執行遊戲規則與流程 | 印出畫面、知道 JSON 細節 |
| `domain/` | 保存動物與園區目前的資料 | 讀取使用者輸入、存檔 |
| `repositories/` | 將資料保存／讀回 | 決定動物會不會餓 |

## 一次餵食的旅程

```text
輸入 Leo
  → main.py 呼叫 game.feed_animal(...)
  → GameService 找到 Leo，檢查食物和飢餓規則
  → Animal.feed(30) 改變 Leo 的 hunger
  → GameService.save_game(state) 交給 Repository
  → JsonGameRepository.save(state) 寫入 JSON 檔
  → 回傳「已餵食 Leo...」給畫面
```

這段流程同時包含教材的四個概念：Data / State、Rules、Interface、Feedback。

## Function 閱讀練習

先不要逐行讀。先填這張表：

| Function | 輸入 | 做什麼 | 輸出／效果 |
| --- | --- | --- | --- |
| `Animal.feed(hunger_reduction)` | 要減少的飢餓 | 改變一隻動物的飢餓 | 回傳新飢餓度 |
| `GameService.feed_animal(state, animal_name)` | 園區狀態、名字 | 檢查並執行餵食 | 回傳給玩家的訊息，並存檔 |
| `JsonGameRepository.save(state)` | 園區狀態 | 寫入 JSON 檔 | 更新 `data/zoo_save.json` |

## 三個 AI Coding 任務

### Level 1：增加顯示資訊

目標：在畫面上顯示每種動物「一天會增加多少飢餓」。

先猜：規則在哪個檔案？顯示又在哪個檔案？請 AI 先提出最小修改計畫。

### Level 2：新增規則

目標：動物健康低於 40 時，餵食一次額外恢復 5 點健康。

先寫清楚：何時觸發？改哪個 State？畫面應回饋什麼？哪些測試要新增？

### Level 3：新增動物

目標：加入 Rabbit，設定牠的每日飢餓與基本收入。

觀察：這項需求不需要複製一個新的 Animal 類別；規則在 `domain/animal_rules.py`，初始資料在 `GameService.start_new_game()`。可直接使用 `templates/new_animal.md`。

## Debug 練習

如果你看到「已餵食」，但關掉再開遊戲後，Leo 的飢餓度又變回原本數字，請沿著這條路檢查：

```text
回饋訊息有出現？
  → GameService 是否真的呼叫 save_game？
  → Repository 是否真的寫入檔案？
  → load 時是否把 JSON 還原成 ZooState？
```

發現問題的位置不一定是真正壞掉的位置。

### 找出專案裡的 Bug

README 提到這個專案裡放了一個 bug。請和 AI 一起：

1. 先試著重現：完整玩完一局，再重新啟動遊戲，結果符合你的預期嗎？
2. 描述現象：哪個操作之後、看到了什麼、預期是什麼？
3. 請 AI 先說明可能原因與證據，再提出最小修正方案；確認後才修改。
4. 修正後重跑測試，並想想：為什麼現有測試沒有抓到它？

講師解答與額外的除錯練習在 `docs/instructor_notes.md`，請先自己試過再看。
