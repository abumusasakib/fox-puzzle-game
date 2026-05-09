# Fox Puzzle Game

This project implements the **Fox Puzzle Game**. The puzzle consists of a 4x4 grid, where tiles labeled "F", "O", and "X" need to be placed in such a way that no forbidden patterns ("FOX" or "XOF") appear in any row, column, or diagonal. The project includes multiple solving approaches and tools to analyze solutions.

## Project Structure

```text
.
├── solver_and_analyzer
│   ├── backtracking_approach.py        # Solver using backtracking technique.
│   ├── board_config.txt               # Input file containing the initial puzzle configuration.
│   ├── random_board_generator.py      # Generates random initial grid configurations for the puzzle.
│   ├── guided_backtracking_approach.py # Guided backtracking solver to fill the grid.
│   ├── monte_carlo_simulation.py      # Monte Carlo simulation-based solver for the puzzle.
│   ├── no_backtracking.py             # Solver that places tiles sequentially without backtracking.
│   ├── csp_solver.py                  # Formal CSP solver using MRV and Forward Checking.
├── README.md                         # Project overview and documentation.
├── fox_game_rules.md                 # Detailed explanation of the Fox Puzzle Game rules.
├── fox_puzzle_game.py                # Main script to play the Fox Puzzle Game.
├── adversarial_fox_game.py             # Competitive version with Alpha-Beta AI.
├── fox_puzzle_game_choose_own_tile.py # Variation where the player chooses their own tiles.
├── fox_puzzle_game_random.py         # Variation with random tile placement.
└── fox_puzzle_game_random_anywhere.py # Variation where random tiles can be placed anywhere.
```

## Overview

The **Fox Puzzle Game** is a logic puzzle where the goal is to fill a 4x4 grid with the tiles labeled "F", "O", and "X" according to the following rules:

- Tiles must be placed in such a way that no "FOX" or "XOF" patterns appear in any row, column, or diagonal.

## Game Classification

Based on the principles of **Adversarial Search** and **Constraint Satisfaction**, the project components are classified as follows:

### 1. Fox Puzzle (Single-Player)

- **Type**: Constraint Satisfaction Problem (CSP).
- **Classification**:
  - **Deterministic**: Outcomes are fixed based on tile placement.
  - **Sequential**: Tiles are placed one at a time.
  - **Perfect Information**: The entire board state is always visible.
- **Goal**: Find a **complete and consistent assignment** of 16 tiles that satisfies all "FOX-avoidance" and "Global Count" constraints.

### 2. Competitive Fox Game (Two-Player)

- **Type**: Zero-Sum Sequential Game.
- **Classification**:
  - **Competitive/Zero-Sum**: One player's win is the other's loss.
  - **Sequential**: Players take turns placing tiles.
  - **Perfect Information**: No hidden information; both players see the grid and remaining tiles.
  - **Deterministic**: No random elements (like dice) influence the rules.
- **Goal**: Use **Minimax** search with **Alpha-Beta Pruning** to avoid completing a "FOX" while maneuvering the opponent into a losing state.

## Solvers and Scripts

The project includes several solvers and tools for analyzing and solving the puzzle.

### Solver Approaches

1. **Backtracking Approach** (`backtracking_approach.py`):
   - This is a depth-first search-based approach to solving the puzzle. It tries placing tiles one by one and uses backtracking when it encounters an invalid configuration.

2. **Guided Backtracking Approach** (`guided_backtracking_approach.py`):
   - An improvement over the basic backtracking approach. It places tiles in a specific order (prioritizing 'O' first) and ensures the "FOX" and "XOF" patterns are avoided using a more directed strategy.

3. **Monte Carlo Simulation** (`monte_carlo_simulation.py`):
   - This solver uses random simulations to attempt to find a valid configuration by placing tiles randomly and checking the validity of the configuration.

4. **No Backtracking Approach** (`no_backtracking.py`):
   - This solver places tiles sequentially in empty spaces. It tries to prioritize 'O', then 'F', then 'X'. If a tile cannot be placed in a cell, it returns a failure.

### Other Files

- **`board_config.txt`**: A text file containing the initial configuration of the board. Empty cells are represented by `_`, and pre-placed tiles are represented by 'F', 'O', or 'X'. This file is used as input for the solvers.
- **`random_board_generator.py`**: Generates random valid initial configurations for the puzzle. This can be used to test the solvers with different starting grids.
- **`fox_game_rules.md`**: Provides a detailed description of the rules of the Fox Puzzle Game.
- **`fox_puzzle_game.py`**: Main script to play the game interactively, allowing users to place tiles and try to solve the puzzle manually.
- **`fox_puzzle_game_choose_own_tile.py`**: A variation of the main game where players can choose the tile to place on the grid.
- **`fox_puzzle_game_random.py`**: A variation of the main game where tiles are placed randomly on the grid.
- **`fox_puzzle_game_random_anywhere.py`**: A variation of the main game where tiles can be placed anywhere on the board randomly.

## Usage

To solve a puzzle using one of the solvers:

1. **Prepare the board configuration**:
   - Create or edit the `board_config.txt` file to provide an initial configuration of the board.

2. **Run the solver**:
   - For backtracking, run:

     ```bash
     python solver_and_analyzer/backtracking_approach.py
     ```

   - For guided backtracking, run:

     ```bash
     python solver_and_analyzer/guided_backtracking_approach.py
     ```

   - For Monte Carlo simulation, run:

     ```bash
     python solver_and_analyzer/monte_carlo_simulation.py
     ```

   - For the no-backtracking approach, run:

     ```bash
     python solver_and_analyzer/no_backtracking.py
     ```

3. **Random Board Generation**:
   - To generate a random board configuration for testing, run:

     ```bash
     python solver_and_analyzer/random_board_generator.py
     ```

## Example

### Example `board_config.txt`

```txt
_ X _ O
O X _ X
_ F F F
X F _ O
```

### Example of Running a Solver

```bash
python solver_and_analyzer/backtracking_approach.py
```

**Output (if a solution is found)**:

```txt
Initial Grid:
_ X _ O
O X _ X
_ F F F
X F _ O

Solved Grid:
F X O O
O X O X
O F F F
X F X O
```

If the configuration is unsolvable, the solver will output:

```txt
No valid configuration found.
```

## Contributing

Feel free to contribute by adding more solving algorithms or improving the existing ones. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
