可以。那我直接先把第一版完整架構規劃書寫出來，之後我們再一起刪東西——**寧可太少，不要為了「看起來像大型系統」硬塞功能。**

這份會刻意讓學生看到正式專案的樣子，但不要求他們先學一堆設計模式。

# Zoo System 開發架構規劃書

## 1. 專案概述

### 1.1 專案名稱

**Zoo System — 動物園動物管理系統**

### 1.2 專案目的

建立一個最小化的動物園管理系統，讓管理員可以查詢動物並執行基本的餵食操作。

本專案的主要目的不是建立一個功能完整的動物園系統，而是展示一個正式軟體專案如何：

- 將大型問題拆成不同模組
- 分離資料、規則與操作流程
- 讓模組透過明確的 Interface 溝通
- 控制模組之間的 Dependency
- 讓功能修改與錯誤排查可以定位
- 使用測試確認修改沒有破壞原本功能

### 1.3 本階段刻意不做的事情

為了保持專案規模小，本版本不包含：

- GUI
- CLI 操作介面
- 登入系統
- 員工管理
- 園區管理
- 飼料庫存
- 真正的資料庫
- 複雜的動物種類系統
- 網路 API

這些功能未來都可以加入，但不是本專案的教學重點。

---

# 2. 核心需求

## 2.1 使用情境

動物園管理員需要餵食動物。

系統需要能夠：

1. 找到指定動物
2. 確認動物目前是否需要餵食
3. 執行餵食
4. 更新動物的狀態
5. 回報餵食結果

---

## 2.2 最小功能需求

### F-01 查詢動物

系統可以依照名稱取得動物。

例如：

```text
find_by_name("Leo")
→ Animal("Leo", "Lion", hunger=80)
```

### F-02 判斷是否可以餵食

動物太飽時不能再次餵食。

例如：

```text
hunger = 80
→ 可以餵食

hunger = 10
→ 已經吃飽，不需要餵食
```

### F-03 餵食動物

餵食後降低動物的飢餓程度。

例如：

```text
餵食前
hunger = 80

餵食後
hunger = 20
```

### F-04 儲存狀態

動物餵食後的狀態需要被保存。

如果系統重新取得該動物，應該仍然知道牠已經被餵過。

---

# 3. 核心資料模型

本專案只有一個核心資料：

## Animal

```text
Animal
├── name
├── species
└── hunger
```

### Data

```text
name
species
```

描述「這隻動物是誰」。

### State

```text
hunger
```

描述「這隻動物目前的狀態」。

例如：

```text
Animal
name = "Leo"
species = "Lion"
hunger = 80
```

餵食之後：

```text
Animal
name = "Leo"
species = "Lion"
hunger = 20
```

因此：

> Data 描述「它是什麼」；State 描述「它現在怎麼樣」。

---

# 4. 系統架構

本專案採用簡單的分層架構：

```text
                    ┌─────────────┐
                    │    main     │
                    │ 程式入口    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   service   │
                    │ 餵食流程    │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
             ┌───────────┐ ┌────────────┐
             │  domain   │ │ repository │
             │ 動物本身  │ │ 資料存取   │
             └───────────┘ └────────────┘
```

各層的責任不同。

---

# 5. 專案目錄

```text
zoo-system/
│
├── src/
│   ├── domain/
│   │   └── animal.py
│   │
│   ├── services/
│   │   └── feeding.py
│   │
│   ├── repositories/
│   │   └── animals.py
│   │
│   └── main.py
│
└── tests/
    └── test_feeding.py
```

---

# 6. Module Responsibility

## 6.1 `domain/animal.py`

### 責任

描述「動物是什麼」。

負責：

- 動物資料
- 動物自身的狀態
- 動物狀態的基本變化

例如：

```text
Animal
├── name
├── species
├── hunger
└── feed()
```

### 不負責

- 從哪裡取得動物
- 資料怎麼儲存
- 使用者怎麼操作
- 餵食流程如何執行

---

## 6.2 `services/feeding.py`

### 責任

描述「餵食這件事情要怎麼執行」。

負責：

- 找到需要處理的動物
- 判斷餵食規則
- 執行餵食
- 儲存修改後的狀態
- 回傳操作結果

例如：

```text
feed_animal(name)
```

### 不負責

- 動物資料本身的定義
- 資料實際儲存格式
- UI

因此 Service 是「流程與商業規則」所在的位置。

---

## 6.3 `repositories/animals.py`

### 責任

處理「動物資料從哪裡來、要存去哪裡」。

提供：

```text
find_by_name(name)
save(animal)
```

Service 不需要知道資料究竟存在：

```text
記憶體
JSON
SQLite
MySQL
API
```

Service 只需要知道 Repository 提供的 Interface。

---

## 6.4 `main.py`

### 責任

作為程式入口。

主要工作：

- 建立需要的物件
- 組合各個 Module
- 啟動主要流程

`main.py` 不應該自己處理：

- 動物規則
- 餵食邏輯
- 資料儲存細節

它比較像「總指揮」，而不是「什麼事情都自己做」。

---

# 7. Interface 設計

Module 不直接依賴彼此的內部實作，而是透過 Interface 溝通。

Repository 提供：

```text
find_by_name(name)
save(animal)
```

Service 只知道：

```text
我要找動物
我要保存動物
```

而不知道：

```text
資料到底存在什麼地方？
```

因此未來可以把：

```text
MemoryRepository
```

換成：

```text
DatabaseRepository
```

Service 不需要重新設計。

---

# 8. Dependency 設計

本專案的 Dependency：

```text
main
 ↓
feeding service
 ↓
animal repository
```

以及：

```text
feeding service
 ↓
animal domain
```

依賴方向應該保持單純。

### Service 可以使用 Domain

因為餵食流程需要操作 Animal。

### Service 可以使用 Repository

因為餵食流程需要取得與保存 Animal。

### Domain 不應該知道 Repository

Animal 不應該知道：

```text
我要存到哪個資料庫？
```

這可以避免 Domain 與資料儲存方式綁死。

---

# 9. Business Logic

本專案至少有一條核心規則：

> 動物已經吃飽時，不能再次餵食。

例如：

```text
hunger > 30
→ 可以餵食

hunger <= 30
→ 不需要餵食
```

這條規則屬於 **Business Logic**。

它不是：

- UI
- Data
- Repository
- 使用者輸入方式

而是「這個系統規定什麼可以做、什麼不能做」。

---

# 10. Feedback

餵食操作完成後，系統需要告訴呼叫者結果。

例如：

```text
FeedResult.SUCCESS
```

或：

```text
FeedResult.ALREADY_FULL
```

或：

```text
FeedResult.ANIMAL_NOT_FOUND
```

Feedback 的目的不是單純「印一句文字」。

它代表：

> 系統完成操作後，將結果交還給上一層。

因此未來即使沒有 CLI，也可以讓其他程式使用這個結果。

---

# 11. 測試策略

本專案至少測試核心商業行為。

### Test 01：正常餵食

```text
Given:
hunger = 80

When:
feed()

Then:
hunger = 20
```

### Test 02：已經吃飽

```text
Given:
hunger = 20

When:
feed_animal()

Then:
狀態不應再次改變
```

### Test 03：找不到動物

```text
Given:
不存在名為 "Unknown" 的動物

When:
feed_animal("Unknown")

Then:
回傳 ANIMAL_NOT_FOUND
```

測試的目的不是測「程式每一行有沒有跑」。

而是確認：

> 系統的重要行為是否符合需求。

---

# 12. Debug 情境

為了展示實際工程中的 Debug 流程，Repository 可以故意出現一個錯誤。

例如：

餵食時：

```text
hunger
80 → 20
```

程式執行當下看起來完全正常。

但重新取得動物後：

```text
hunger
20 → 80
```

表示餵食結果沒有被正確保存。

此時不應直接修改：

```text
feeding.py
```

而應沿著資料流追查：

```text
餵食
 ↓
Animal 狀態有沒有改？
 ↓
Service 有沒有呼叫 save？
 ↓
Repository 有沒有收到正確資料？
 ↓
Repository 有沒有真的保存 hunger？
```

最終可能發現：

```text
Repository.save()
```

只保存了：

```text
name
species
```

卻漏掉：

```text
hunger
```

這就是一個很好的工程 Debug 案例：

> 「看到錯誤」不等於「錯誤就在看到錯誤的地方」。

---

# 13. Extension：加入 Penguin

未來需求：

> 動物園新增企鵝。

新增：

```text
Penguin
```

理想情況下，只需要修改與動物資料或相關規則直接有關的部分。

不應該因為新增一種動物，就修改：

```text
main.py
feeding.py
repository
tests
```

中所有不相關的部分。

這可以觀察架構是否具有：

> **Change Localization — 變更局部化**

好的架構不是「永遠不用改程式」。

而是：

> 新需求進來時，可以很快知道應該改哪裡，而且不需要到處亂改。

---

# 14. Clean Code 要求

本專案不強制使用複雜 Design Pattern。

只要求幾個基本原則：

### 14.1 清楚命名

避免：

```text
a
b
do_it()
```

使用：

```text
animal
repository
feed_animal()
```

### 14.2 函式只做一件主要事情

例如：

```text
find_by_name()
```

負責找資料。

不要同時：

```text
找資料
印畫面
修改狀態
存檔
```

### 14.3 不讓不同責任互相污染

不要讓：

```text
Animal
```

知道：

```text
JSON 怎麼存
```

也不要讓：

```text
Repository
```

決定：

```text
動物什麼時候可以吃飯
```

### 14.4 優先保持簡單

本專案不為了「看起來專業」而加入：

- 不必要的 Design Pattern
- 多層抽象
- 大量 Interface
- 複雜繼承
- 不需要的 Framework

架構的目標是降低複雜度，而不是製造複雜度。

---

# 15. AI Coding 開發規則

AI 可以負責實作，但不得自行決定整個系統架構。

開發時提供給 AI 的資訊應包含：

```text
目前要修改的功能
↓
相關 Module
↓
Interface
↓
不可修改的範圍
↓
驗收條件
```

例如：

> 請修改餵食功能，使 hunger <= 30 時不能再次餵食。
>
> 只能修改 `services/feeding.py`。
>
> 不要修改 Repository 與 Domain。
>
> 完成後說明修改原因，並提出需要新增或修改的測試。

AI 完成後由人負責：

```text
Review
 ↓
Test
 ↓
確認是否符合需求
```

---

# 16. 開發流程

本專案採用：

```text
需求
 ↓
Understand
理解問題
 ↓
Locate
找到相關 Module
 ↓
Plan
規劃修改方式
 ↓
Ask AI
讓 AI 實作
 ↓
Review
檢查 AI 修改
 ↓
Test
驗證結果
 ↓
Debug
發現問題後定位責任範圍
```

因此：

> AI 不負責「想完整個專案」。

AI 是實作工具。

人需要知道：

- 要改什麼
- 為什麼改
- 應該改哪裡
- 哪些地方不能動
- 怎樣才算完成

---

# 17. 架構總覽

最終學生看到的專案可以濃縮成：

```text
                     Zoo System
                         │
                       main
                         │
                         ▼
                ┌─────────────────┐
                │ Feeding Service │
                │   餵食流程/規則  │
                └───────┬─────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌────────────┐      ┌────────────┐
       │   Animal   │      │ Repository │
       │ 資料/狀態  │      │ 資料存取   │
       └────────────┘      └────────────┘
                                  │
                                  ▼
                            實際資料來源
```

而整個專案其實只做一件事：

```text
把一隻動物餵飽。
```

這正是本專案的設計目的：

> **功能很小，但架構是真實的。**

學生不用先做出一個「大型動物園」。

他們只需要打開這個專案，就能看到：

```text
一個需求
 ↓
被拆成多個責任
 ↓
責任被放進不同 Module
 ↓
Module 透過 Interface 溝通
 ↓
main 組合它們
 ↓
tests 驗證行為
 ↓
出錯時沿著 Dependency 定位
 ↓
新需求只修改必要的地方
```

這就是正式專案的基本樣子。

這版我刻意**沒有把「專業」做成一堆框架和設計模式**。下一步我們可以直接拿這份逐項驗收：**你的「Function / Module / Interface / Data / State / Rules / Feedback / Dependency / Main / Test / Debug / Extension / AI Coding」每一個概念到底有沒有真的在這個專案裡看得見。**