# 🗺️ Wumpus World — AI Logic Game

> A Python implementation of the classic **Wumpus World** AI problem, featuring both a graphical (GUI) version and a terminal-based version. Built using **Knowledge Bases**, **Inference Engines**, and **Agent-based reasoning** — core concepts from Artificial Intelligence.

---

## 📖 Table of Contents

- [About the Game](#-about-the-game)
- [AI Concepts Demonstrated](#-ai-concepts-demonstrated)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [How to Play](#-how-to-play)
- [Installation & Running](#-installation--running)
- [Scoring System](#-scoring-system)
- [Tech Stack](#-tech-stack)

---

## 🎮 About the Game

The **Wumpus World** is a classic AI environment introduced by Gregory Yob in 1973 and later popularized in the textbook *Artificial Intelligence: A Modern Approach* (Russell & Norvig).

The player (agent) navigates a grid-based cave, collecting gold while avoiding deadly hazards:

| Symbol | Entity | Description |
|--------|--------|-------------|
| 🧌 | **Wumpus** | A monster that kills you on contact. You sense it by a nearby **stench**. |
| 🕳️ | **Pit** | A bottomless pit. You sense it by a nearby **breeze**. |
| 💰 | **Gold** | The treasure you must collect. You sense it by a nearby **glimmer**. |
| 🧭 | **Agent** | You! Starting at position (1, 1). |

**Goal:** Navigate the cave, grab the gold, and climb back out from position (1, 1) — alive!

---

## 🧠 AI Concepts Demonstrated

This project implements three foundational AI components:

### 1. Knowledge Base (KB)
Stores the state of the world — the positions of the Wumpus, gold, and pits. The KB is initialized with randomly placed entities and updated as the agent interacts with the environment.

### 2. Inference Engine
Reasons over the KB to generate **percepts** (sensory inputs) for the agent:
- 👃 **Stench** → Wumpus is in an adjacent room
- 💨 **Breeze** → A pit is in an adjacent room
- ✨ **Glimmer** → Gold is in the current or adjacent room

### 3. Rational Agent
The agent uses percepts to decide actions. It tracks its position, score, and remaining moves, making decisions based on the information inferred from the environment.

---

## ✨ Features

- 🖼️ **Graphical GUI** using `tkinter` with image-based rendering (Player, Wumpus, Gold sprites)
- 🖥️ **Terminal-based** version for a text-driven experience
- 🔄 **Restart** button to reset the game without reopening the application
- 📊 **Live score tracking** with move counter
- ⚠️ **Hazard detection** — immediate game-over on Wumpus or Pit encounters
- 🎲 **Randomized world** — each game generates a new layout
- 🔢 **Configurable grid size** (default: 4×4)

---

## 📁 Project Structure

```
wumpus_game/
│
├── code_gui.py          # GUI version — full tkinter interface with sprite images
├── import random.py     # Terminal/console version — text-based gameplay
│
├── Player.png           # Agent sprite image
├── Wumpus.png           # Wumpus sprite image
├── Gold.png             # Gold sprite image
│
└── AI report.pptx       # Project report/presentation
```

### Key Classes

| Class | File | Responsibility |
|-------|------|----------------|
| `KnowledgeBase` | `code_gui.py` | Stores world state (Wumpus, gold, pits, grid) |
| `InferenceEngine` | `code_gui.py` | Derives percepts from KB for the agent |
| `Agent` | `code_gui.py` | Handles movement, grabbing gold, scoring, and climbing |
| `Visualization` | `code_gui.py` | Renders the game grid and controls via tkinter |
| `WumpusWorld` | `import random.py` | All-in-one class for the console version |

---

## 🕹️ How to Play

### Controls (GUI Version)

| Button | Action |
|--------|--------|
| ⬆️ Up | Move agent north |
| ⬇️ Down | Move agent south |
| ⬅️ Left | Move agent west |
| ➡️ Right | Move agent east |
| 💎 Grab | Pick up gold if in the same room |
| 🧗 Climb | Exit the cave (only from position (1,1) with gold) |
| 🔄 Restart | Reset the game |

### Controls (Terminal Version)

```
Enter your action: left / right / up / down / grab / release / shoot / quit
```

### Percepts (Clues)

- **"You smell a stench."** → Wumpus is adjacent
- **"You feel a breeze."** → Pit is adjacent
- **"You see a glimmer of gold."** → Gold is nearby
- **"The room feels safe."** → No immediate threats

---

## ⚙️ Installation & Running

### Prerequisites

- Python 3.x
- `tkinter` (usually bundled with Python on Windows/macOS)

### Run the GUI Version

```bash
# Clone the repository
git clone https://github.com/your-username/wumpus-world.git
cd wumpus-world

# Run the graphical version
python code_gui.py
```

> ⚠️ **Note:** `Player.png`, `Wumpus.png`, and `Gold.png` must be in the same directory as `code_gui.py` for images to load correctly.

### Run the Terminal Version

```bash
python "import random.py"
```

---

## 🏆 Scoring System

| Action | Points |
|--------|--------|
| Each move | **-1** |
| Grab gold | **+20** |
| Fall into pit / Eaten by Wumpus | **Game Over** |
| Successfully climb out with gold | **Win!** |

- Maximum moves per game: **20**
- Running out of moves ends the game

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core language |
| **tkinter** | GUI framework for the graphical version |
| **random** | World generation (random placement of entities) |

---

## 📚 Background

This project is based on the **Wumpus World** problem described in:

> Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

It demonstrates **logical agents**, **knowledge representation**, and **propositional reasoning** — foundational topics in AI.

---

## 👩‍💻 Author

**Tasneem** — AI & Computer Science Enthusiast
