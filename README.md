# Zoo System 動物園餵食小程式

這是一個給 Python 初學者閱讀的小專案。它示範如何用函式和字典找到動物、餵食動物，以及用測試檢查結果。

程式只使用 Python 內建功能，不需要安裝套件、不需要建置，也不需要資料庫。

## 開始使用

需要 Python 3.9 或更新版本。在專案資料夾開啟終端機：

```powershell
python --version
python main.py
python -m unittest discover -s tests -v
```

執行程式會餵食 Leo，並顯示餵食結果和新的飢餓值。`hunger` 越大代表越餓：

```text
餵食成功。
Leo (Lion) hunger: 20
```

## 專案檔案

```text
Zoo_manager/
├── .gitignore
├── README.md
├── arc_plan_init.md
├── docs/
│   └── learning_guide.md
├── main.py
└── tests/
    └── test_main.py
```

- `main.py`：動物資料、查找動物、餵食規則和程式入口都放在同一個檔案，方便初學者順著讀完。
- `tests/test_main.py`：使用 Python 內建的 `unittest` 測試程式行為。
- `docs/learning_guide.md`：用簡單步驟介紹程式和練習方式。
- `arc_plan_init.md`：原始開發計畫，保留作為需求背景；目前程式刻意簡化，沒有採用計畫中較進階的介面與分層。

## 餵食規則

- 動物用字典表示，包含 `name`、`species` 和 `hunger`。
- 動物用清單收在一起。
- 飢餓值大於 30 時可以餵食，每次減少 60，最低不會低於 0。
- 飢餓值小於或等於 30 時不再餵食。
- 找不到動物時會回報訊息。
- 資料只存在程式執行期間；重新啟動後會重新建立範例資料。

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
