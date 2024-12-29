# README

## 簡介

這是一個基於 Python 開發的遊戲應用程式，結合了 Tkinter 圖形介面和遊戲邏輯。玩家可以選擇不同模式進行遊戲，透過隨機生成符號及特殊模式觸發，達成更高分數。程式還支援分數上傳功能，方便儲存玩家的紀錄。

## 創作背景

2023年的那個夏天，治平高中商務二孝的那個本壘板 🍚🐟 正處於很無聊的狀態，於是想到國昌老師教的 [MIT App Inventor 2](https://ai2.appinventor.mit.edu/) 的存在，想無聊做個小遊戲，運用以前玩 Minecraft 做紅石機關的邏輯、從手機相簿裡面隨便找的幾張圖片，以及網路上隨便抓的垃X音效與音樂，於是第一代啦八機誕生了。

後續陸續新增了 超級阿禾模式(SuperHHH)、綠光阿瑋模式(GreenWei)、皮卡丘充電(PiKaChu) 等模式。

2024年8月，🍚🐟已經高中畢業，即將進入大學，去買了人生第一台電腦，為了學習 Python，於是一邊透過用Python還原啦八機，一邊學習相關知識，最終誕生了此 Repository。

## 功能特點

- 支援多種遊戲模式：
  - 普通模式。
  - 超級阿禾模式（SuperHHH）。
  - 綠光阿瑋模式（GreenWei）。
  - 皮卡丘充電模式（PiKaChu）。
- 使用 `.json` 文件模擬數據運行。
- 整合了音效及圖片資源，提供豐富的視覺與聽覺體驗。
- 遊戲分數的即時顯示與歷史最高分數記錄。
- 分數提交到 Google 表單。

## 遊戲邏輯流程

1. **遊戲開始**：
   - 玩家從首頁輸入名稱，選擇進入普通模式或模擬模式。

2. **隨機生成符號**：
   - 每回合會隨機生成三個符號，根據符號組合計算分數。
   - 機率受到當前遊戲模式的影響，例如普通模式與特殊模式機率不同。

3. **特殊模式觸發**：
   - 當符號滿足特定條件時，將觸發以下特殊模式並進入特殊背景與切換背景音樂：
     - **超級阿禾 (SuperHHH)**：增加分數倍率，同時出現三個超級阿禾會獲得加倍分。
     - **綠光阿瑋 (GreenWei)**：分數獲取翻倍，可透過累積特定符號觸發。
     - **皮卡丘充電 (PiKaChu)**：延長遊戲次數，並可以觸發其他特殊模式。

4. **分數計算**：
   - 根據符號匹配的類型和數量，計算邊際分數，且普通模式與特殊模式機率不同，會根據模式進行倍率加成，
   - 實時更新當前分數與歷史最高分數。

5. **遊戲結束**：
   - 回合結束後顯示玩家的最終得分。
   - 支援重新開始或退出遊戲。

## 安裝與使用

### 系統與環境需求

- Python 3.9 或更高版本。
- 必須安裝以下 Python 套件：
  - `tkinter`
  - `pygame`
  - `Pillow`

### 安裝方式

1. 確保您的系統安裝了 Python。

2. 使用以下命令安裝必要的依賴：

   ```bash
   pip install pygame Pillow
   ```

3. 複製此項目：

   ```bash
   git clone https://github.com/Yorn90104/LABAG-PY-PJ.git
   ```

4. 進入程式目錄。

5. 執行 `yield.py` 文件產生 `imageb64.py` 與 `soundb64.py`：

   ```bash
   python yield.py
   ```

6. 執行 `main.py` 文件:

   ```bash
   python main.py
   ```

7. 根據指引進行遊戲。
   若想使用 `.json` 檔案執行模擬，請在 `main.py` 中:

   ```python
   Game.setup_path(".\\248119875.json") #更改為你的 .json 檔案路徑
   ```

## 檔案結構

```plaintext
├── main.py            # 主程式
├── GUI               # 圖形介面相關模組 [GUI-simplify-Tkinter-Pygame-](https://github.com/Yorn90104/GUI-simplify-Tkinter-Pygame-.git)
│   └── __init__.py
├── src               # 遊戲邏輯與資源
│   ├── element.py
│   ├── imageb64.py   # 圖片資源的 Base64 編碼
│   ├── soundb64.py   # 音效資源的 Base64 編碼
│   └── game.py       # 遊戲邏輯
├── tide.py           # 將此資料夾下的 .py 檔案彙整成單一 .txt 檔案 (PY.txt)
├── PY.txt            # 可上傳至 ChatGPT 使其說明此程式內容
├── Target.py         # 達成目標分數模擬工具
├── TargetJson.py     # 基於 Target.py 再增加產生 .json 檔案的工具
├── yield.py          # 產生 imageb64.py 與 soundb64.py 的 Base64 編碼 檔案
├── README.md         # 說明文件
└── Superhhh.ico      # 打包用的圖標
```

## 注意事項

1. `yield.py` 程式會解碼 Base64 圖像與音效，請勿隨意刪除 `src` 與 `Asset` 資料夾內的資源檔案。
2. 遊戲過程中的臨時文件會在結束時自動刪除。
3. 若遇到問題，請確保已安裝正確版本的依賴，並參考錯誤訊息進行調試。
4. 若欲自行打包成單一 .exe 文件 (無其他依賴檔案)，可於程式目錄使用已下命令:

   ```bash
   pyinstaller --windowed -F --icon=Superhhh.ico Main.py  
   ```

## 版權聲明

此項目由 🍚🐟 創建，僅供學習與娛樂用途。所有音樂與圖片素材均來源於公開資源，若有侵權請聯繫刪除。

---

# README (English Version)

## Introduction

This is a Python-based game application that integrates Tkinter for the graphical interface and game logic. Players can choose different modes to play, achieve higher scores through randomly generated symbols, and trigger special modes. The program also supports score upload functionality, enabling players to save their records.

## Background

In the summer of 2023, 🍚🐟, a student from the Business class of Zhih-Ping High School, found themselves feeling bored. Inspired by the MIT App Inventor 2 taught by Mr. Kuo, they decided to create a simple game using their knowledge of Minecraft redstone logic, random images from their phone gallery, and sound effects/music sourced online. Thus, the first version of LABA Machine was born.

Subsequent updates introduced modes such as SuperHHH, GreenWei, and PiKaChu.  

By August 2024, 🍚🐟 had graduated from high school and was preparing for college. They purchased their first computer and started learning Python. While recreating LABA Machine in Python, they honed their programming skills, culminating in this repository.

## Features

- Supports multiple game modes:
  - Standard mode.
  - **SuperHHH** mode.
  - **GreenWei** mode.
  - **PiKaChu** mode.
- Uses `.json` files for data simulation.
- Integrated sound effects and images for an immersive experience.
- Real-time score display and historical high score tracking.
- Supports score submission to Google Forms.

## Game Logic and Flow

1. **Game Start**:
   - Players input their name on the homepage and choose to enter either Standard or Simulation mode.

2. **Random Symbol Generation**:
   - Each round generates three random symbols. Scores are calculated based on symbol combinations.
   - Probabilities are influenced by the selected game mode.

3. **Special Mode Triggers**:
   - Special modes activate when symbols meet specific conditions, switching to unique backgrounds and music:
     - **SuperHHH**: Score multipliers apply, and scoring three SuperHHH symbols grants double points.
     - **GreenWei**: Doubles score acquisition, triggered by accumulating specific symbols.
     - **PiKaChu**: Extends the number of turns and may trigger other special modes.

4. **Score Calculation**:
   - Scores are calculated based on the type and quantity of matched symbols.
   - Multipliers are applied depending on the mode.

5. **Game End**:
   - Displays the player's final score at the end of the round.
   - Options to restart or exit the game.

## Installation and Usage

### System and Environment Requirements

- Python 3.9 or later.
- Required Python libraries:
  - `tkinter`
  - `pygame`
  - `Pillow`

### Installation Steps

1. Ensure Python is installed on your system.

2. Install the required dependencies using the following command:

   ```bash
   pip install pygame Pillow
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/Yorn90104/LABAG-PY-PJ.git
   ```

4. Navigate to the project directory.

5. Execute the `yield.py` file to generate `imageb64.py` and `soundb64.py`:

   ```bash
   python yield.py
   ```

6. Run the `main.py` file to start the game:

   ```bash
   python main.py
   ```

7. Follow the prompts to play the game.  
   If you want to use a `.json` file for simulation, modify `main.py` as follows:

   ```python
   Game.setup_path(".\\248119875.json") # Replace with the path to your .json file
   ```
   
## File Structure

```plaintext
├── main.py            # Main program
├── GUI               # GUI modules [GUI-simplify-Tkinter-Pygame-](https://github.com/Yorn90104/GUI-simplify-Tkinter-Pygame-.git)
│   └── __init__.py
├── src               # Game logic and resources
│   ├── element.py
│   ├── imageb64.py   # Base64 encoded image resources
│   ├── soundb64.py   # Base64 encoded sound resources
│   └── game.py       # Game logic
├── tide.py           # Combines .py files in this folder into a single .txt file (PY.txt)
├── PY.txt            # Uploadable to ChatGPT for explanation
├── Target.py         # Target score simulation tool
├── TargetJson.py     # Adds .json generation functionality to Target.py
├── yield.py          # Generates imageb64.py and soundb64.py from Base64 encoded assets
├── README.md         # Documentation
└── Superhhh.ico      # Icon for packaging
```

## Notes

1. The `yield.py` script decodes Base64 images and sounds. Do not delete the `src` and `Asset` folders.
2. Temporary files created during gameplay will be automatically deleted after the game ends.
3. If issues arise, ensure the correct dependencies are installed and troubleshoot using error messages.
4. To package the program into a standalone `.exe` file, use the following command in the project directory:

   ```bash
   pyinstaller --windowed -F --icon=Superhhh.ico Main.py  
   ```

## License

This project was created by 🍚🐟 for educational and entertainment purposes only. All music and image assets are sourced from public resources. For copyright concerns, please contact for removal.