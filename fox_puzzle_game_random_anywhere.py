import tkinter as tk
from tkinter import messagebox
import random

# Initialize game variables
initial_tiles = ['F'] * 5 + ['O'] * 6 + ['X'] * 5  # predefined tile counts
tile_sequence = []  # will store the shuffled sequence
grid_size = 4
grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
attempt_count = 0  # Track the number of attempts

# Function to shuffle tiles and start a new game
def shuffle_tiles():
    global tile_sequence, grid, attempt_count
    attempt_count += 1  # Increment attempt count each time the game is reset
    tile_sequence = initial_tiles[:]  # copy the initial list
    random.shuffle(tile_sequence)  # randomize tile order
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    # Clear the buttons
    for i in range(grid_size):
        for j in range(grid_size):
            buttons[i][j].config(text="", state="normal")
    
    # Update the attempt count and remaining tile counts display
    update_attempt_count()
    update_remaining_tile_counts()

# Function to check if placing a tile at a random position is valid
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

# Function to place a random tile where the user clicks
def place_tile_on_click(row, col):
    if grid[row][col] != '':  # Check if the cell is already occupied
        messagebox.showerror("Invalid Move", "This cell is already occupied!")
        return

    if len(tile_sequence) == 0:
        messagebox.showinfo("End of Game", "All tiles have been placed.")
        return

    # Randomly pick a tile from the remaining tiles
    tile = random.choice(tile_sequence)
    
    if is_valid_placement(row, col, tile):
        # Place the tile
        grid[row][col] = tile
        buttons[row][col].config(text=tile, state="disabled")
        tile_sequence.remove(tile)  # Remove the placed tile from the list
    else:
        messagebox.showerror("Invalid Placement", f"Placing {tile} here creates 'FOX' or 'XOF'!")
        shuffle_tiles()
        return

    # Update the remaining tiles display
    update_remaining_tile_counts()

# Function to update the remaining tile counts display
def update_remaining_tile_counts():
    count_F = tile_sequence.count('F')
    count_O = tile_sequence.count('O')
    count_X = tile_sequence.count('X')
    
    remaining_tiles_label.config(text=f"Remaining F's: {count_F}  O's: {count_O}  X's: {count_X}")

# Function to update the attempt count display
def update_attempt_count():
    attempt_count_label.config(text=f"Attempts: {attempt_count}")

# Initialize the main window
root = tk.Tk()
root.title("FOX Puzzle Game")
root.geometry("400x500")

# Create a grid of buttons
buttons = []
for i in range(grid_size):
    row_buttons = []
    for j in range(grid_size):
        button = tk.Button(root, text="", width=5, height=2, font=("Arial", 16), state="normal", 
                           command=lambda i=i, j=j: place_tile_on_click(i, j))
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), command=shuffle_tiles)
reset_button.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

# Attempt count label
attempt_count_label = tk.Label(root, text=f"Attempts: {attempt_count}", font=("Arial", 12))
attempt_count_label.grid(row=grid_size + 1, column=0, columnspan=grid_size, pady=10)

# Remaining tile counts label
remaining_tiles_label = tk.Label(root, text=f"Remaining F's: 5  O's: 6  X's: 5", font=("Arial", 12))
remaining_tiles_label.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=10)

# Start the first game
shuffle_tiles()

# Run the application
root.mainloop()
