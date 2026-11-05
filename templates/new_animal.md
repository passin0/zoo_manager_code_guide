# 新增動物底稿

## 設計資料

<!-- 先決定數值再寫程式。可以參考 domain/animal_rules.py 裡現有三種動物的數值。 -->

| 欄位 | 填寫內容 | 說明 |
| --- | --- | --- |
| 種類名稱（英文） |  | 程式用來查規則的名字，例如 `Lion` |
| 顯示名字 |  | 玩家餵食時要輸入的名字，例如 `Leo` |
| 初始飢餓度 |  | 0～100，新遊戲開始時的飢餓度 |
| 每日增加飢餓度 |  | 每結束一天增加多少 |
| 健康 100 時的每日收入 |  | 健康越低，實際收入越少 |

## 步驟 1：加入規則

打開 `domain/animal_rules.py`，在 `ANIMAL_RULES` 裡加一行：

```python
ANIMAL_RULES = {
    # 這是一個「字典」（dict）：冒號左邊是 key，右邊是 value。
    # key 是種類名稱，value 是另一個字典，存放這種動物的規則。
    "Lion": {"hunger_increase": 25, "daily_income": 8},
    "Penguin": {"hunger_increase": 15, "daily_income": 6},
    "Monkey": {"hunger_increase": 20, "daily_income": 5},
    # 在這裡新增一行，格式和上面相同，結尾記得加逗號：
    # "種類名稱": {"hunger_increase": 每日增加飢餓度, "daily_income": 每日收入},
}
```

## 步驟 2：加入初始動物

打開 `services/game_service.py`，找到 `start_new_game()`，在動物清單中加一隻：

```python
state = ZooState(
    1,   # 第幾天
    20,  # 初始資金
    12,  # 初始食物
    [
        # 這是一個「串列」（list），用中括號包住，每個項目用逗號分隔。
        # Animal(顯示名字, 種類名稱, hunger=初始飢餓度) 會建立一隻動物。
        # 種類名稱必須和步驟 1 的 key 完全一樣（大小寫也要相同），否則結束一天時會出錯。
        Animal("Leo", "Lion", hunger=40),
        Animal("Pipi", "Penguin", hunger=25),
        Animal("Momo", "Monkey", hunger=55),
        # 在這裡新增一行：
        # Animal("顯示名字", "種類名稱", hunger=初始飢餓度),
    ],
)
```

## 步驟 3：新增測試

在 `tests/test_game_service.py` 的 `GameServiceTests` 類別裡加一個方法：

```python
    # 方法名稱必須以 test_ 開頭，unittest 才會把它當成測試執行。
    def test_new_animal_gets_hungrier_at_end_of_day(self):
        # self.state 是 setUp() 建立好的新遊戲，已經包含你新增的動物。
        self.game.end_day(self.state)

        # find_animal("名字") 會找出那隻動物；.hunger 取得牠的飢餓度。
        # assertEqual(實際值, 預期值)：兩者不相等時測試就會失敗。
        # 預期值 = 初始飢餓度 + 每日增加飢餓度（最多 100）。
        self.assertEqual(self.state.find_animal("顯示名字").hunger, 預期值)
```

## 步驟 4：跑全部測試

```powershell
python -m unittest discover -s tests -v
```

預期會有一個原本的測試失敗。請找出是哪一個、為什麼失敗，先自己算出新的預期值，再決定如何更新它。

## 不需要修改

- 不需要建立新的動物類別檔案；所有動物共用 `domain/animal.py` 的 `Animal`。
- 不需要修改 Repository；存檔會自動包含新動物。
- 不需要修改 `main.py` 或 `ui/console.py`；畫面會自動列出所有動物。

## 注意

新動物只會出現在新遊戲。若已經有舊存檔，請在選單選「重新開始」。
