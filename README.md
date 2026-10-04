# 小小動物園：AI Coding 教學範例

這是一個可以直接玩的迷你動物園遊戲，也是給「可能還沒寫過程式」的同學閱讀 AI 生成專案的練習素材。

你不必先背 Python。這個專案要練習的是：看懂一個功能經過哪些模組、先規劃再請 AI 修改，以及用測試確認結果。

## 先玩一次

本專案只使用 Python 內建功能。請在專案資料夾開啟終端機：

```powershell
python main.py
```

遊戲會自動建立存檔；離開後再次執行會接續原本的狀態。選擇「重新開始」即可建立全新的動物園。

若你的電腦無法使用 `python` 指令，請先安裝 Python 3.9 以上，並在安裝時勾選加入系統 PATH。

## 玩家規則

- 照顧 Lion、Penguin、Monkey 三隻動物，經營到第 7 天。
- 餵食消耗 1 份食物，讓飢餓降低 30。
- 每天結束時，每種動物依自己的規則變餓。
- 飢餓度 80 以上會失去 15 點健康；30 以下會恢復 5 點健康。
- 健康越好，動物園每天的收入越高。
- 任一動物健康降到 0，遊戲失敗。
- 遊戲結束時輸入名字，最後資金會存入記分板並顯示前五名。

## 專案地圖

```text
Zoo_manager/
├── main.py                    # 程式入口：接收玩家選擇
├── ui/
│   └── console.py              # 顯示畫面與回饋
├── services/
│   └── game_service.py         # 遊戲規則與操作流程
├── domain/
│   ├── animal.py               # 一隻動物的資料與狀態
│   ├── zoo_state.py            # 整座動物園的狀態
│   └── animal_rules.py         # 各種類動物的差異規則
├── repositories/
│   ├── game_repository.py      # 存檔工具應提供的介面
│   └── json_game_repository.py # JSON 存檔的實作
│   ├── scoreboard_repository.py # 記分板應提供的介面
│   └── json_scoreboard_repository.py # 記分板 JSON 的實作
├── docs/
│   └── lesson_map.md           # 課堂閱讀與練習指引
└── tests/                      # 核心規則與存檔測試
```

最重要的流程是：

```text
玩家操作 → UI → GameService → Domain + Repository → 回饋給玩家
```

詳見 [教學地圖](docs/lesson_map.md)。

要增加功能時，先讀 [擴充指南](docs/extension_guide.md)，並從 [templates](templates/README.md) 複製功能變更單，而不是直接要求 AI 重寫專案。

## 執行測試

```powershell
python -m unittest discover -s tests -v
```

測試不是要證明「程式沒有任何問題」，而是確認重要規則仍符合我們寫下的期待：餵食、每日變化、過度飢餓與存檔讀取。

## 給 AI 的第一個練習

不要立刻要求 AI 修改。先試著問：

```text
請不要修改程式。依 README、docs/lesson_map.md 與檔案結構，整理：
1. 每個模組的主要責任；
2. 餵食 Leo 會經過哪些 function；
3. 哪些判斷是你從程式確認的事實，哪些只是推測。
```

接著再選擇 `docs/lesson_map.md` 裡的一個 Level 任務，要求 AI 先提出最小修改計畫與驗收方式。
