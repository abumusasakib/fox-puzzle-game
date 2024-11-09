# FOX Puzzle Game

The FOX Puzzle Game is a fun and challenging puzzle game where players place tiles marked with 'F', 'O', and 'X' onto a grid, following specific placement rules. The objective is to fill the grid without creating the forbidden patterns "FOX" or "XOF" in any direction (horizontal, vertical, or diagonal).

This project contains the following files and directories:

## Folder Structure

```text
.
├── fox_game_rules.md
├── fox_puzzle_game_choose_own_tile.py
├── fox_puzzle_game_random.py
└── solver_and_analyzer
    ├── fox_game_solver.py
    ├── guided_backtracking_approach.py
    ├── monte_carlo_simulation.py
    └── no_backtracking.py
```

## Files Overview

### `fox_game_rules.md`

This file contains the detailed rules of the FOX Puzzle Game, explaining how the game is played and the logic behind tile placements.

### `fox_puzzle_game_choose_own_tile.py`

This script allows players to choose their own tiles to place on the grid. It includes the basic logic for tile placement, validation, and grid updates.

### `fox_puzzle_game_random.py`

This script allows players to automatically place tiles on the grid in a randomized order. The grid is updated after each move, and the game will check for invalid patterns that would create "FOX" or "XOF".

### `solver_and_analyzer/`

This directory contains various scripts for solving and analyzing the FOX Puzzle game, including different approaches to tile placement.

#### `fox_game_solver.py`

This script provides a solver that attempts to find valid solutions to the FOX Puzzle game. It's the main entry point for solving the puzzle automatically.

#### `guided_backtracking_approach.py`

This script implements a guided backtracking approach to solve the puzzle. It explores potential moves and backtracks if a solution is invalid, ultimately finding a valid solution or determining that it's unsolvable.

#### `monte_carlo_simulation.py`

This script uses Monte Carlo simulations to analyze the puzzle and find solutions through random sampling and statistical methods. It provides an insight about the solution space of the puzzle.

#### `no_backtracking.py`

This script attempts to solve the puzzle without using backtracking. Instead, it uses a more straightforward approach, focusing on immediate valid placements.

## How to Play

1. **Choose a Tile**: You can either manually choose which tile ('F', 'O', or 'X') to place on the grid or use the randomized script to shuffle the tiles for you.

2. **Tile Placement Rules**: Place the tiles onto the grid in such a way that no row, column, or diagonal forms the forbidden patterns "FOX" or "XOF".

3. **Game Completion**: The game ends when all tiles are placed correctly, or if an invalid move occurs. If the latter happens, the game will inform you that the move is invalid and you will have to reset the game.

4. **Attempts**: Every time you reset the game, the attempt count will increase, allowing you to track your progress.

## Solving the Puzzle

The `solver_and_analyzer/` directory contains several scripts that aim to solve the puzzle automatically.

- **Backtracking Approach**: Use `guided_backtracking_approach.py` to attempt solving with backtracking.
- **Monte Carlo Simulation**: Use `monte_carlo_simulation.py` to explore the solution space of the puzzle.
- **No Backtracking**: Try the straightforward approach in `no_backtracking.py` if you want a solution without backtracking.

## Requirements

- Python 3.x
- Tkinter for the GUI (it should be installed by default with Python)

## How to Run

1. **Run the Game**:
   - To play the game with manual tile selection, run:

     ```bash
     python fox_puzzle_game_choose_own_tile.py
     ```

   - To play the game with randomized tile placement, run:

     ```bash
     python fox_puzzle_game_random.py
     ```

2. **Use Solver**:
   - To use the game solver with backtracking, run:

     ```bash
     python solver_and_analyzer/guided_backtracking_approach.py
     ```

   - To see the solution space using Monte Carlo simulations, run:

     ```bash
     python solver_and_analyzer/monte_carlo_simulation.py
     ```

   - To solve without backtracking, run:

     ```bash
     python solver_and_analyzer/no_backtracking.py
     ```
