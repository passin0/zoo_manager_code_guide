# 小小動物園 Zoo Manager

一款用終端機遊玩的迷你動物園經營遊戲，也是 AI Coding 課程的閱讀與修改練習專案。

專案只使用 Python 標準函式庫，裝好 Python 就能執行，不需要額外安裝套件。結構拆成數個小模組，方便追蹤「一個操作經過哪些程式」。
專案中預留了一個 bug，練習方式請見 [挑戰指南](docs/challenge_guide.md)。

## 快速開始

需求：Python 3.9 以上（建議搭配 VS Code 與 Python 擴充套件）。

可以先在終端機輸入下面這行確認環境，顯示 `Python 3.9` 以上的版本號即可：

```powershell
python --version
```

在專案資料夾開啟終端機並執行：

```powershell
python main.py
```

遊戲會自動建立存檔，離開後再次執行會接續原本的進度；在選單選「重新開始」可建立全新的動物園。

## 遊戲規則

- 照顧 Lion、Penguin、Monkey 三隻動物，經營到第 7 天。
- 餵食消耗 1 份食物，讓飢餓度降低 30。
- 每天結束時，每種動物依自己的規則增加飢餓度。
- 飢餓度 80 以上會失去 15 點健康；30 以下會恢復 5 點健康。
- 健康越好，動物園每天的收入越高。
- 任一動物健康降到 0，遊戲失敗。
- 遊戲結束時輸入名字，最後資金會存入記分板並顯示前五名。

## 專案結構

```text
zoo_manager_code_guide/
├── main.py                              # 程式入口：接收玩家選擇
├── ui/
│   └── console.py                       # 顯示畫面與回饋
├── services/
│   └── game_service.py                  # 遊戲規則與操作流程
├── domain/
│   ├── animal.py                        # 一隻動物的資料與狀態
│   ├── zoo_state.py                     # 整座動物園的狀態
│   └── animal_rules.py                  # 各種動物的差異規則與數值
├── repositories/
│   ├── game_repository.py               # 遊戲存檔的介面
│   ├── json_game_repository.py          # 遊戲存檔的 JSON 實作
│   ├── scoreboard_repository.py         # 記分板的介面
│   └── json_scoreboard_repository.py    # 記分板的 JSON 實作
├── docs/
│   ├── challenge_guide.md               # 閱讀、擴充與除錯的挑戰指南
│   └── instructor_notes.md              # 講師筆記（含解答）
├── templates/                           # 修改前填寫的工作底稿
├── tests/                               # 單元測試
└── data/                                # 執行後自動產生的存檔（不進版控）
```

## 架構

```text
玩家操作 → main.py / ui → GameService → Domain + Repository → 回饋給玩家
```

| 層 | 位置 | 負責 |
| --- | --- | --- |
| 介面（UI） | `main.py`、`ui/` | 收取玩家輸入、顯示狀態與訊息 |
| 服務（Service） | `services/` | 遊戲規則與操作流程 |
| 領域（Domain） | `domain/` | 動物與園區的資料、狀態變化 |
| 儲存（Repository） | `repositories/` | 將狀態保存到檔案、從檔案讀回 |

## 執行測試

```powershell
python -m unittest discover -s tests -v
```

測試涵蓋餵食、每日變化、過度飢餓、存檔讀取與記分板。

## 文件

- [挑戰指南](docs/challenge_guide.md)：如何閱讀專案、需求該改哪裡、挑戰任務與除錯練習。
- [工作底稿](templates/README.md)：修改前要填寫的模板。
