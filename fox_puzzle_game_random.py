import tkinter as tk
from tkinter import messagebox
import random

# Initialize game variables
initial_tiles = ['F'] * 5 + ['O'] * 6 + ['X'] * 5  # predefined tile counts
tile_sequence = []  # will store the shuffled sequence
grid_size = 4
grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
current_position = 0  # Start at the top-left corner

# Function to shuffle tiles and start a new game
def shuffle_tiles():
    global tile_sequence, current_position, grid
    tile_sequence = initial_tiles[:]  # copy the initial list
    random.shuffle(tile_sequence)  # randomize tile order
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    current_position = 0
    # Clear the buttons
    for i in range(grid_size):
        for j in range(grid_size):
            buttons[i][j].config(text="", state="normal")

# Function to check if placing a tile at the current position is valid
def is_valid_placement(row, col, tile):
    # Define directions to check for patterns: horizontal, vertical, and two diagonals
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

# Place the next tile automatically
def place_next_tile():
    global current_position
    row, col = divmod(current_position, grid_size)
    if current_position < len(tile_sequence):
        tile = tile_sequence[current_position]
        if is_valid_placement(row, col, tile):
            # Place the tile
            grid[row][col] = tile
            buttons[row][col].config(text=tile, state="disabled")
            current_position += 1
            if current_position == grid_size * grid_size:
                messagebox.showinfo("Completed", "Puzzle completed successfully!")
        else:
            messagebox.showerror("Invalid Placement", f"Placing {tile} here creates 'FOX' or 'XOF'!")
            messagebox.showinfo("End of Game", "Bad luck! Reset the game and try again.")
    else:
        messagebox.showinfo("End of Game", "All tiles have been placed.")

# Initialize the main window
root = tk.Tk()
root.title("FOX Puzzle Game")
root.geometry("400x500")

# Create a grid of buttons
buttons = []
for i in range(grid_size):
    row_buttons = []
    for j in range(grid_size):
        button = tk.Button(root, text="", width=5, height=2, font=("Arial", 16), state="normal")
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Place tiles button
place_button = tk.Button(root, text="Place Next Tile", font=("Arial", 14), command=place_next_tile)
place_button.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), command=shuffle_tiles)
reset_button.grid(row=grid_size + 1, column=0, columnspan=grid_size, pady=10)

# Start the first game
shuffle_tiles()

# Run the application
root.mainloop()
