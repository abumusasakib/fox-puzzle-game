import tkinter as tk
from tkinter import messagebox

# Initialize the game variables
initial_tiles = {'F': 5, 'O': 6, 'X': 5}
remaining_tiles = initial_tiles.copy()
grid_size = 4
grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
current_position = [0, 0]  # Start at the top-left corner
attempt_count = 0
game_active = True

# Function to reset the game
def reset_game():
    global remaining_tiles, grid, current_position, attempt_count, game_active
    attempt_count += 1
    remaining_tiles = initial_tiles.copy()
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    current_position = [0, 0]
    game_active = True
    
    # Reset buttons on the grid
    for i in range(grid_size):
        for j in range(grid_size):
            buttons[i][j].config(text="", state="normal")
    
    # Update remaining tiles and attempt count displays
    update_remaining_tiles()
    update_attempt_count()

# Function to check if placing a tile at the current position is valid
def is_valid_placement(row, col, tile):
    # Define directions to check for patterns: horizontal, vertical, and diagonals
    directions = [
        (0, 1), (1, 0), (1, 1), (1, -1)  # Right, Down, Diagonal Down-Right, Diagonal Down-Left
    ]
    
    for dr, dc in directions:
        # Collect characters in both forward and backward directions
        forward_pattern, backward_pattern = [tile], [tile]
        for i in range(1, 3):  # Look two tiles forward and backward
            # Forward
            nr, nc = row + i * dr, col + i * dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                forward_pattern.append(grid[nr][nc])
            # Backward
            nr, nc = row - i * dr, col - i * dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                backward_pattern.insert(0, grid[nr][nc])
        
        # Check if forward or backward pattern forms "FOX" or "XOF"
        if ''.join(forward_pattern) == "FOX" or ''.join(forward_pattern) == "XOF" or \
           ''.join(backward_pattern) == "FOX" or ''.join(backward_pattern) == "XOF":
            return False
    return True

# Function to place a tile on the grid
def place_tile(tile):
    global current_position, game_active
    row, col = current_position

    if not game_active:
        messagebox.showerror("Game Over", "Invalid move detected. Please reset the game and try again.")
        return

    if remaining_tiles[tile] <= 0:
        messagebox.showerror("Error", f"No remaining {tile} tiles!")
        return

    if is_valid_placement(row, col, tile):
        # Place the tile
        grid[row][col] = tile
        buttons[row][col].config(text=tile, state="disabled")
        remaining_tiles[tile] -= 1

        # Move to the next position
        if col == grid_size - 1:
            if row == grid_size - 1:
                # Puzzle completed
                messagebox.showinfo("Completed", "Puzzle completed successfully!")
                return
            current_position = [row + 1, 0]
        else:
            current_position = [row, col + 1]

        # Update remaining tiles display
        update_remaining_tiles()
    else:
        messagebox.showerror("Invalid Move", f"Placing {tile} here creates 'FOX' or 'XOF'!")
        game_active = False
        messagebox.showinfo("Game Over", "Please reset the game and try again.")

# Function to update the display of remaining tiles
def update_remaining_tiles():
    remaining_tiles_label.config(
        text=f"Remaining Tiles - F: {remaining_tiles['F']}, O: {remaining_tiles['O']}, X: {remaining_tiles['X']}"
    )

# Function to update the attempt count display
def update_attempt_count():
    attempt_count_label.config(text=f"Attempts: {attempt_count}")

# Initialize the main window
root = tk.Tk()
root.title("FOX Puzzle Game")
root.geometry("400x550")

# Create a grid of buttons
buttons = []
for i in range(grid_size):
    row_buttons = []
    for j in range(grid_size):
        button = tk.Button(root, text="", width=5, height=2, font=("Arial", 16), state="normal")
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Tile selection frame
frame = tk.Frame(root)
frame.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

tk.Label(frame, text="Select a Tile:", font=("Arial", 14)).pack(side="left")

# Tile selection buttons
for tile in "FOX":
    btn = tk.Button(frame, text=tile, font=("Arial", 14), command=lambda t=tile: place_tile(t))
    btn.pack(side="left", padx=5)

# Remaining tiles display
remaining_tiles_label = tk.Label(root, text="", font=("Arial", 12))
remaining_tiles_label.grid(row=grid_size + 1, column=0, columnspan=grid_size, pady=5)
update_remaining_tiles()

# Reset button and attempt counter
reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), command=reset_game)
reset_button.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=5)

attempt_count_label = tk.Label(root, text=f"Attempts: {attempt_count}", font=("Arial", 12))
attempt_count_label.grid(row=grid_size + 3, column=0, columnspan=grid_size, pady=10)

# Run the application
root.mainloop()
