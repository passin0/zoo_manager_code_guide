# 新增玩家操作底稿

例如加入「治療動物」或「購買食物」。

## 行為定義

<!-- 先用文字定義清楚，再寫程式。 -->

- 操作名稱：
- 玩家輸入：<!-- 選單數字之外，還要輸入什麼？例如動物名字、購買數量。 -->
- 成功條件：
- 失敗條件：<!-- 例如：找不到動物、錢不夠、輸入不是數字。 -->
- 要改變的狀態：<!-- ZooState 的 day / money / food，或某隻 Animal 的 hunger / health。 -->
- 成功／失敗回饋：

## 步驟 1：在 GameService 新增方法

打開 `services/game_service.py`，在 `GameService` 類別裡新增一個方法。
以下用「治療動物」示範結構，請依你的需求修改：

```python
    # def 定義一個方法。self 代表 GameService 自己，state 是整座動物園的狀態，
    # animal_name 是玩家輸入的名字。
    def heal_animal(self, state, animal_name):
        # (1) 找出目標：find_animal 找不到時會回傳 None。
        animal = state.find_animal(animal_name)

        # (2) 檢查規則：每個不允許的情況都先 return 一段失敗訊息，方法會在這裡結束。
        if animal is None:
            return "找不到這隻動物，請確認名字。"
        if state.money < 10:
            return "資金不足，治療需要 $10。"

        # (3) 更新狀態：只透過 Animal 提供的方法改數值，不要直接寫 animal.health = ...
        animal.change_health(20)
        state.money -= 10  # -= 的意思是「減去後再存回去」，等於 state.money = state.money - 10

        # (4) 存檔：每個成功的操作都要呼叫，否則重開遊戲後變化會消失。
        self.save_game(state)

        # (5) 回傳訊息：format() 會把 {} 依序換成後面的值。
        return "已治療 {}，健康變成 {}。".format(animal.name, animal.health)
```

> 規則數值（例如 10、20）建議放到 `domain/animal_rules.py` 成為常數，像現有的 `FEED_COST`。

## 步驟 2：寫測試

複製 `templates/new_rule_test.py.example` 到 `tests/`，至少測試：

- 成功的情況；
- 找不到動物；
- 資源不足。

## 步驟 3：接上選單

打開 `main.py`，在 `while` 迴圈裡的 `if / elif` 加一個分支：

```python
        # elif 是「否則如果」：前面的條件都不成立時，才檢查這一個。
        elif choice == "4":
            # input() 會顯示提示文字並等待玩家輸入；.strip() 去掉前後空白。
            name = input("要治療哪一隻動物？").strip()
            # main.py 只負責呼叫方法、拿到訊息，規則都寫在 GameService。
            result = game.heal_animal(state, name)
```

## 步驟 4：更新畫面

在 `ui/console.py` 的 `show_help()` 加上新選項，讓玩家看得到：

```python
    print("4. 治療動物")
```

## 給 AI 的檢查問題

- 新規則是否誤寫在 `main.py` 或 UI？
- 成功後是否呼叫 `save_game(state)`？
- 失敗時是否沒有改到任何狀態？
- UI 是否只顯示回傳訊息，而沒有自行修改資料？
