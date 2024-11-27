import tkinter as tk
from tkinter import messagebox
import random

# Initialize game variables
initial_tiles = ["F"] * 5 + ["O"] * 6 + ["X"] * 5  # predefined tile counts
tile_sequence = []  # will store the shuffled sequence
grid_size = 4
grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
attempt_count = 0  # Track the number of attempts
game_mode = "random"  # Default game mode
remaining_tiles = {"F": 5, "O": 6, "X": 5}  # Track the remaining tiles of each type


# Function to shuffle tiles and start a new game
def shuffle_tiles():
    global tile_sequence, grid, remaining_tiles, attempt_count
    if remaining_tiles != {
        "F": 5,
        "O": 6,
        "X": 5,
    }:  # Don't increment if the remaining tiles haven't changed
        attempt_count += 1  # Increase attempt count
    tile_sequence = initial_tiles[:]  # copy the initial list
    random.shuffle(tile_sequence)  # randomize tile order
    grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    remaining_tiles = {"F": 5, "O": 6, "X": 5}  # Reset the remaining tiles

    # Clear the buttons
    for i in range(grid_size):
        for j in range(grid_size):
            buttons[i][j].config(
                text="", state="normal" if game_mode == "choose" else "disabled"
            )

    # Update the attempt count display and tile count display
    update_attempt_count()
    update_remaining_tiles()


# Function to check if placing a tile at the current position is valid
def is_valid_placement(row, col, tile):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),  # Right, Down, Diagonal Down-Right, Diagonal Down-Left
    ]

    for dr, dc in directions:
        forward_pattern, backward_pattern = [tile], [tile]
        for i in range(1, 3):  # Look two tiles forward and backward
            nr, nc = row + i * dr, col + i * dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                forward_pattern.append(grid[nr][nc])
            nr, nc = row - i * dr, col - i * dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                backward_pattern.insert(0, grid[nr][nc])

        if (
            "".join(forward_pattern) == "FOX"
            or "".join(forward_pattern) == "XOF"
            or "".join(backward_pattern) == "FOX"
            or "".join(backward_pattern) == "XOF"
        ):
            return False
    return True


# Function to check for "FOX" or "XOF" in the grid after each move
def check_game_over():
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] != "":
                if not is_valid_placement(i, j, grid[i][j]):
                    return True  # Game over condition met
    return False


# Place the next tile randomly on an empty spot
def place_random_tile(max_attempts=1000):
    global tile_sequence
    if len(tile_sequence) > 0:
        available_tiles = [t for t in tile_sequence if remaining_tiles[t] > 0]
        if available_tiles:
            # Randomly choose an empty spot on the grid
            empty_spots = [
                (i, j)
                for i in range(grid_size)
                for j in range(grid_size)
                if grid[i][j] == ""
            ]

            if not empty_spots:
                check_game_over_condition()
                return

            if len(available_tiles) == 1:  # Special case for the last tile
                tile = available_tiles[0]
                row, col = empty_spots[0]
                grid[row][col] = tile
                buttons[row][col].config(text=tile, state="disabled")
                remaining_tiles[tile] -= 1  # Decrease the remaining tile count
                tile_sequence.remove(tile)  # Remove the placed tile from the list
            else:
                row, col = random.choice(empty_spots)
                tile = random.choice(available_tiles)  # Get a random tile from the remaining ones
                remaining_tiles[tile] -= 1  # Decrease the remaining tile count
                tile_sequence.remove(tile)  # Remove the placed tile from the list

                if is_valid_placement(row, col, tile):
                    grid[row][col] = tile
                    buttons[row][col].config(text=tile, state="disabled")
                else:
                    tile_sequence.append(tile)  # Revert the tile placement
                    remaining_tiles[tile] += 1  # Increase the remaining tile count
                    if max_attempts > 0:
                        place_random_tile(max_attempts - 1)  # Recursively call to place the next valid tile
                    else:
                        messagebox.showerror("Error", "Unable to place tile after 1000 attempts.")

            update_remaining_tiles()  # Update the displayed remaining tiles

            if check_game_over():
                messagebox.showinfo(
                    "Game Over", "You created a 'FOX' or 'XOF' pattern! Game Over!"
                )
                shuffle_tiles()  # Reset the game
            elif len(tile_sequence) == 0:  # All tiles are placed
                check_game_over_condition()
        else:
            messagebox.showerror("Error", "No available tiles to place.")
    else:
        messagebox.showinfo("End of Game", "No more tiles to place!")


# Function to handle manual tile placement in Choose Mode
def place_tile_manually(row, col):
    global tile_sequence
    if game_mode == "choose" and grid[row][col] == "":
        available_tiles = [
            t for t in tile_sequence if remaining_tiles[t] > 0
        ]  # Get a random tile from the remaining ones
        if available_tiles:
            tile = random.choice(
                available_tiles
            )  # Get a random tile from the remaining ones
            if remaining_tiles[tile] > 0:
                remaining_tiles[tile] -= 1  # Decrease the remaining tile count
                tile_sequence.pop(0)  # Remove the placed tile from the list
                grid[row][col] = tile
                buttons[row][col].config(text=tile, state="disabled")
                update_remaining_tiles()  # Update remaining tiles count after placement

                if check_game_over():
                    messagebox.showinfo(
                        "Game Over", "You created a 'FOX' or 'XOF' pattern! Game Over!"
                    )
                    shuffle_tiles()  # Reset the game
                elif len(tile_sequence) == 0:  # All tiles are placed
                    check_game_over_condition()
            else:
                messagebox.showerror("Error", f"No remaining {tile} tiles!")


# Function to check game-over condition when all tiles are placed
def check_game_over_condition():
    if check_game_over():
        messagebox.showinfo(
            "Game Over", "You created a 'FOX' or 'XOF' pattern! Game Over!"
        )
        shuffle_tiles()  # Reset the game
    else:
        messagebox.showinfo(
            "Game Over",
            "All tiles placed without forming 'FOX' or 'XOF' patterns. Well Done!",
        )
        shuffle_tiles()  # Reset the game


# Function to update the attempt count display
def update_attempt_count():
    attempt_count_label.config(text=f"Attempts: {attempt_count}")


# Function to update the remaining tiles display
def update_remaining_tiles():
    remaining_label.config(
        text=f"Remaining F's: {remaining_tiles['F']}, O's: {remaining_tiles['O']}, X's: {remaining_tiles['X']}"
    )


# Show help with game rules
def show_help():
    help_text = """
    FOX Puzzle Game Rules:
    
    1. The grid size is 4x4, and the tiles consist of the letters 'F', 'O', and 'X'.
    2. In each turn, place a tile (either 'F', 'O', or 'X') on an empty spot on the grid.
    3. You must avoid forming the words "FOX" or "XOF" in any direction (horizontal, vertical, or diagonal).
    4. Once you place a tile, check if you form the pattern "FOX" or "XOF". If you do, the game ends.
    5. The game can be played in two modes:
        - Random Mode: The tiles are placed randomly on the grid.
        - Choose Your Own Tile: You choose where to place each tile.
    """
    messagebox.showinfo("Game Rules", help_text)


# Function to switch game modes
def switch_game_mode(mode):
    global game_mode, attempt_count
    game_mode = mode
    shuffle_tiles()  # Reset the game and tiles
    attempt_count = 0  # Reset the attempt count when switching game modes

    # Enable/disable buttons based on game mode
    for i in range(grid_size):
        for j in range(grid_size):
            buttons[i][j].config(state="normal" if mode == "choose" else "disabled")

    update_game_mode_display()  # Update the game mode label


# Function to update the game mode display
def update_game_mode_display():
    game_mode_label.config(text=f"Game Mode: {game_mode.capitalize()}")


# Initialize the main window
root = tk.Tk()
root.title("FOX Puzzle Game")
root.geometry("400x650")

# Create a grid of buttons
buttons = []
for i in range(grid_size):
    row_buttons = []
    for j in range(grid_size):
        button = tk.Button(
            root,
            text="",
            width=5,
            height=2,
            font=("Arial", 16),
            state="disabled",
            command=lambda i=i, j=j: place_tile_manually(i, j),
        )
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Place tiles button
place_button = tk.Button(
    root, text="Place Random Tile", font=("Arial", 14), command=place_random_tile
)
place_button.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

# Reset button
reset_button = tk.Button(
    root, text="Reset Game", font=("Arial", 14), command=shuffle_tiles
)
reset_button.grid(row=grid_size + 1, column=0, columnspan=grid_size, pady=10)

# Game mode label
game_mode_label = tk.Label(
    root, text=f"Game Mode: {game_mode.capitalize()}", font=("Arial", 12)
)
game_mode_label.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=10)

# Remaining tiles label
remaining_label = tk.Label(
    root,
    text=f"Remaining F's: {remaining_tiles['F']}, O's: {remaining_tiles['O']}, X's: {remaining_tiles['X']}",
    font=("Arial", 12),
)
remaining_label.grid(row=grid_size + 3, column=0, columnspan=grid_size, pady=10)

# Attempt count label
attempt_count_label = tk.Label(
    root, text=f"Attempts: {attempt_count}", font=("Arial", 12)
)
attempt_count_label.grid(row=grid_size + 4, column=0, columnspan=grid_size, pady=10)

# Game mode buttons
random_mode_button = tk.Button(
    root,
    text="Random Mode",
    font=("Arial", 12),
    command=lambda: switch_game_mode("random"),
)
random_mode_button.grid(row=grid_size + 5, column=0, columnspan=2, pady=10)

choose_mode_button = tk.Button(
    root,
    text="Choose Mode",
    font=("Arial", 12),
    command=lambda: switch_game_mode("choose"),
)
choose_mode_button.grid(row=grid_size + 5, column=2, columnspan=2, pady=10)

# Help button
help_button = tk.Button(root, text="Help", font=("Arial", 12), command=show_help)
help_button.grid(row=grid_size + 6, column=0, columnspan=grid_size, pady=10)

# Start the first game
shuffle_tiles()

# Run the application
root.mainloop()
