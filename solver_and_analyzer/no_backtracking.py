# Initialize tile counts and an empty 4x4 grid
remaining_tiles = {'F': 5, 'O': 6, 'X': 5}
grid = [['' for _ in range(4)] for _ in range(4)]

# Function to check if placing a tile at (row, col) is valid
def is_valid_placement(grid, row, col, tile):
    # Avoid "FOX" and "XOF" patterns by checking already placed neighbors
    directions = [
        (-1, 0), (0, -1), # Up and Left
        (-1, -1), (-1, 1) # Top-left diagonal and Top-right diagonal
    ]
    for dr, dc in directions:
        pattern = [tile]
        for i in range(1, 3): # Look up to 2 tiles away in each direction
            nr, nc = row + i * dr, col + i * dc
            if 0 <= nr < 4 and 0 <= nc < 4 and grid[nr][nc]:
                pattern.insert(0, grid[nr][nc]) if i == 2 else pattern.append(grid[nr][nc])
            else:
                break
        # Check for forbidden "FOX" or "XOF" patterns
        if ''.join(pattern) in ['FOX', 'XOF']:
            return False
    return True

# Place tiles in sequential order from 1 to 16
def place_tiles_sequentially():
    index = 0
    for row in range(4):
        for col in range(4):
            for tile in 'OFX':  # Prioritize placing "O" first, then "F", then "X"
                if remaining_tiles[tile] > 0 and is_valid_placement(grid, row, col, tile):
                    grid[row][col] = tile
                    remaining_tiles[tile] -= 1
                    break
            else:
                # If no tile can be placed, indicate failure
                return False
    return True  # Successfully filled the grid

# Execute the tile placement
if place_tiles_sequentially():
    # Display the resulting grid if successful
    for row in grid:
        print(" ".join(row))
else:
    print("No valid configuration found.")
