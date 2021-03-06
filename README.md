# UAV

## Environment
Linux + Python 2

## Installation
```bash
# 下載 code
$ git clone https://github.com/DyslexiaS/UAV
```

這裡還要安裝 dronekit, opencv2, 設定環境變數等等。

## Execute

### 1. 連上 UAV
```bash
# 到 drone 資料夾
$ cd UAV/drone

# 後面數字（不給的話預設爲1） 0 表示無線連接， 1 表示有線連接。
# 如通過 raspberry pi 連線可以跑以下指令：
$ python connect.py 1
```

等待一段時間（我記得要幾十秒）會出現以下 output 等待輸入指令，表示連接成功。
```
...
#################
execute: （這裡可以輸入接下來介紹的 4 種指令，通常是輸入 takeoff 就可以了）
```

### 2. 執行任務

支援 4 個指令：
+ `takeoff [height] [n]` 指令：讓 UAV 起飛。
  + 可以輸入 `takeoff 10` 讓無人機飛起 `10` 米，高度自訂。
  + **`takeoff` 之後會直接進入 `control` 指令**。
  + `[height]` 可以不給，預設值爲 `5`。
  + `[n]` 可以不給，預設值爲 `0`，用於 `detect` 指令。

+ `control [n]` 指令：鍵盤控制 UAV 活動。
  + 分別用 `w` `a` `s` `d` 和 `i` `j` `k` `l` 模擬遙控器左右手柄。
  + `p`：相等於執行 `detect n 0`（拍一張）。
  + `o`：相等於執行 `detect n 1`（連續拍）。
  + `m`：相等於執行 `mode guided`，切換成 `GUIDED` 模式。（我記得是 `GUIDED` 模式才能電腦控制，若過程中已經由遙控器切換成其他模式，要記得先切回 `GUIDED`）
  + `q`：退出 `control` 模式。
  + `[n]` 可以不給，預設值爲 `0`，用於 `detect` 指令。

+ `detect [n] [auto]` 指令：辨識圓及自動控制飛行方向
  + `[n]` 可以爲任意數字，和拍照存的圖片名稱相關，預設值爲0。每次拍照都將命名爲 `idx_高度.jpg` 存在 `img/` 資料夾，作爲後續研究用。
  + `[auto]` 可以爲 `0` 或 `1`。
  + `[auto]` 爲 `0` 表示拍一次照然後按分析結果方向飛行。（不太會用到）
  + `[auto]` 爲 `1` 表示持續拍照及根據判斷結果飛行，可中途輸入 `Ctrl+C` 退出。
+ `mode [some mode]` ：切換 mode
  + `[some mode]` 可以切換的大部分模式（不確定是不是全部），如 `mode guided` 進入 `GUIDED` 模式。


### 3. 圓的辨識與飛行方向的控制規則

1. 通過提取目標顏色、灰階處理、圖像平滑、霍爾變換找到圓心。（每張找到圓心的圖片也都會存在 `img/` 裡）
2. 依據圓的直徑反推 UAV 高度。（其實照理來說第1、2的步驟反了，但這是因爲我記得飛行中直接讀 UAV 的高度會非常不準。若這部分解決了可以進一步改善第一步，即我們可以推算這高度拍照的圓的直徑的像素距離，降低找錯圓的機率）
3. 根據高度推算 UAV 與圓心的實際距離。
4. 設定 UAV 的水平速度（正比於實際距離，但有上限）及垂直速度（根據 UAV 與圓心的俯角，若大於 45 度則向下飛，反之向上）。
5. 若找不到圓將垂直向上擴大拍照範圍。
