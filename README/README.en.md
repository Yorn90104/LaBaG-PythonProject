# LaBaG

## Introduction

This is a Python-based game application that integrates Tkinter for the graphical interface and game logic. Players can choose different modes to play, achieve higher scores through randomly generated symbols, and trigger special modes. The program also supports score upload functionality, enabling players to save their records.

## Background

In the summer of 2023, 🍚🐟, a student from the Business class of Zhih-Ping High School, found themselves feeling bored. Inspired by the MIT App Inventor 2 taught by Mr. Kuo-Chang, they decided to create a simple game using their knowledge of Minecraft redstone logic, random images from their phone gallery, and sound effects/music sourced online. Thus, the first version of LABA Machine was born.

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

5. Execute the `yieldb64.py` file to generate `imageb64.py` and `soundb64.py`:

   ```bash
   python yieldb64.py
   ```

6. Run the `main.py` file to start the game:

   ```bash
   python main.py
   ```

7. Follow the prompts to play the game.  
   
## File Structure

```plaintext
├── main.py           # Main program
├── GUI               # GUI modules 
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
├── yieldb64.py       # Generates imageb64.py and soundb64.py from Base64 encoded assets
├── README.md         # Documentation
└── Superhhh.ico      # Icon for packaging
```

## Notes

1. The `yieldb64.py` script decodes Base64 images and sounds. Do not delete the `src` and `Asset` folders.
2. Temporary files created during gameplay will be automatically deleted after the game ends.
3. If issues arise, ensure the correct dependencies are installed and troubleshoot using error messages.
4. To package the program into a standalone `.exe` file, use the following command in the project directory:

   ```bash
   pyinstaller --windowed -F --icon=Superhhh.ico Main.py  
   ```

## Resources Links

- [MIT App Inventor 2](https://ai2.appinventor.mit.edu/)
- [Pygame Official Documentation](https://www.pygame.org/docs/)
- [GUI-simplify-Tkinter-Pygame-](https://github.com/Yorn90104/GUI-simplify-Tkinter-Pygame-.git)


