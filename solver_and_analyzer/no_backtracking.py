# Initialize tile counts
remaining_tiles = {'F': 5, 'O': 6, 'X': 5}

# Function to read the grid from the file
def create_grid_from_file(file_path):
    """
    Reads a 4x4 board configuration from a file and returns it as a 2D list.
    """
    grid = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                grid.append(line.strip().split())
        if len(grid) != 4 or any(len(row) != 4 for row in grid):
            raise ValueError("The grid must be a 4x4 configuration.")
        return grid
    except Exception as e:
        print(f"Error reading grid: {e}")
        return None

# Function to check if placing a tile at (row, col) is valid
def is_valid_placement(grid, row, col, tile):
    """
    Checks if placing the tile at (row, col) is valid by ensuring no "FOX" or "XOF" patterns are formed.
    """
    # Avoid "FOX" and "XOF" patterns by checking already placed neighbors
    directions = [
        (-1, 0), (0, -1), # Up and Left
        (-1, -1), (-1, 1) # Top-left diagonal and Top-right diagonal
    ]
    for dr, dc in directions:
        pattern = [tile]
        for i in range(1, 3):  # Look up to 2 tiles away in each direction
            nr, nc = row + i * dr, col + i * dc
            if 0 <= nr < 4 and 0 <= nc < 4 and grid[nr][nc]:
                pattern.insert(0, grid[nr][nc]) if i == 2 else pattern.append(grid[nr][nc])
            else:
                break
        # Check for forbidden "FOX" or "XOF" patterns
        if ''.join(pattern) in ['FOX', 'XOF']:
            return False
    return True

# Function to place tiles in the grid sequentially, prioritizing "O", then "F", then "X"
def place_tiles_sequentially(grid):
    """
    Fills the grid by sequentially placing tiles while respecting the "FOX" and "XOF" constraints.
    """
    index = 0
    for row in range(4):
        for col in range(4):
            if grid[row][col] == '_':  # Only fill empty cells
                for tile in 'OFX':  # Prioritize placing "O" first, then "F", then "X"
                    if remaining_tiles[tile] > 0 and is_valid_placement(grid, row, col, tile):
                        grid[row][col] = tile
                        remaining_tiles[tile] -= 1
                        break
                else:
                    # If no tile can be placed, return failure
                    return False
    return True  # Successfully filled the grid

# Main function to solve the puzzle
def main():
    input_file = "board_config.txt"  # Input file name
    grid = create_grid_from_file(input_file)
    if grid is None:
        return

    print("Initial Grid:")
    for row in grid:
        print(" ".join(row))

    # Calculate initial remaining tiles based on the current grid
    for row in grid:
        for tile in row:
            if tile in remaining_tiles:
                remaining_tiles[tile] -= 1

    # Solve the puzzle by placing tiles sequentially
    if place_tiles_sequentially(grid):
        print("\nSolved Grid:")
        for row in grid:
            print(" ".join(row))
    else:
        print("\nNo valid configuration found.")

if __name__ == "__main__":
    main()
