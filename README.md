# Zoo System 動物園餵食小程式

這是一個給 Python 初學者閱讀的小專案。玩家每天照顧動物、使用飼料、維持健康並累積收益，也可以從程式中學習函式、字典和簡單的類別繼承。

程式只使用 Python 內建功能，不需要安裝套件、不需要建置，也不需要資料庫。

## 開始使用

需要 Python 3.9 或更新版本。在專案資料夾開啟終端機：

```powershell
python --version
python main.py
python -m unittest discover -s tests -v
```

執行遊戲：

```text
python main.py
```

每天開始時動物會變餓。玩家可以選擇餵動物或結束今天；結束時會更新健康、增加收益，然後進入下一天。

## 專案檔案

```text
Zoo_manager/
├── .gitignore
├── README.md
├── arc_plan_init.md
├── docs/
│   └── learning_guide.md
├── animals/
│   ├── animal.py
│   ├── lion.py
│   ├── elephant.py
│   └── penguin.py
├── feeding/
│   ├── feeder.py
│   └── food.py
├── main.py
└── tests/
    ├── test_animals.py
    ├── test_game.py
    └── test_main.py
```

- `main.py`：每日遊戲流程、遊戲狀態和程式入口。
- `animals/animal.py`：基本動物類別，管理名字、飢餓度和健康。
- `animals/lion.py`、`animals/elephant.py`、`animals/penguin.py`：動物都繼承 `Animal`，並各自提供食物和每日飢餓增加量。
- `feeding/food.py`、`feeding/feeder.py`：設定飼料消耗量和餵食規則。
- `tests/`：使用 Python 內建的 `unittest` 測試動物、遊戲循環與舊有字典範例。
- `docs/learning_guide.md`：用簡單步驟介紹程式和練習方式。
- `arc_plan_init.md`：原始開發計畫，保留作為需求背景；目前程式刻意簡化，沒有採用計畫中較進階的介面與分層。

## 遊戲規則

- 飢餓度範圍是 0 到 100；越高代表越餓。
- 每天開始時，獅子增加 20 點飢餓度，企鵝增加 15 點，大象增加 10 點。
- 每次餵食會消耗 2 份飼料，並降低 40 點飢餓度；動物只吃自己適合的食物。
- 每天結束時，飢餓度 70 以上的動物健康減少 10；飢餓度 30 以下的動物健康增加 2。
- 每天結束會獲得 $5 收益，並進入下一天。
- 動物健康和飢餓度都不會低於 0 或高於 100。

## 動物類別和繼承

每種動物都可以使用 `Animal` 的飢餓和健康功能，也有自己的食物和叫聲：

```python
from animals.lion import Lion

leo = Lion("Leo", hunger=60)
leo.start_day()        # 新的一天開始，飢餓度增加
leo.eat("肉")          # 吃對食物後，飢餓度降低
```

`Lion(Animal)` 表示 `Lion` 繼承 `Animal`。所有動物共用相同的每日狀態更新方法，個別類別只設定自己的食物、飢餓速度和叫聲。

## 字典版餵食函式

`main.py` 仍保留 `find_animal` 和 `feed_animal`，示範用字典和函式處理動物資料；遊戲本身使用動物類別。

- 字典版餵食範例沿用原本的 `name`、`species` 和 `hunger` 格式。
- 遊戲狀態只存在程式執行期間；重新啟動後會重新開始。

## Git 入門

此專案已初始化 Git。查看檔案狀態：

```powershell
git status
```

確認要保存的檔案後，可以加入並提交：

```powershell
git add .gitignore README.md main.py tests docs arc_plan_init.md
git commit -m "Simplify zoo tutorial for beginners"
```

`.gitignore` 會略過 Python 快取等不需要保存的檔案。
