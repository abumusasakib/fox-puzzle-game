import copy

# Initialize tile counts (must match the total number of tiles needed)
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

# Function to check if the current grid is valid
def is_valid(grid):
    """
    Checks if placing any tile on the current grid violates the "FOX" or "XOF" patterns
    in any row, column, or diagonal.
    """
    # Check rows, columns, and diagonals for invalid patterns "FOX" or "XOF"
    for i in range(4):
        # Check rows and columns
        row = "".join(grid[i])
        col = "".join([grid[j][i] for j in range(4)])
        if "FOX" in row or "XOF" in row or "FOX" in col or "XOF" in col:
            return False

    # Check diagonals
    diag1 = "".join([grid[i][i] for i in range(4)])
    diag2 = "".join([grid[i][3-i] for i in range(4)])
    if "FOX" in diag1 or "XOF" in diag1 or "FOX" in diag2 or "XOF" in diag2:
        return False

    # Check 2x2 subgrids
    for i in range(3):
        for j in range(3):
            subgrid = "".join([grid[i][j], grid[i][j+1], grid[i+1][j], grid[i+1][j+1]])
            if "FOX" in subgrid or "XOF" in subgrid:
                return False

    return True

# Backtracking function to attempt filling the grid
def solve(grid, row, col):
    # Check if we are done (end of the grid)
    if row == 4:
        return grid

    # Move to the next row if we reach the end of a column
    if col == 4:
        return solve(grid, row + 1, 0)

    # If the cell is already filled, move to the next cell
    if grid[row][col] != '_':
        return solve(grid, row, col + 1)

    # Try placing each tile
    for tile in 'FOX':
        if remaining_tiles[tile] > 0:
            # Place the tile and decrease its count
            grid[row][col] = tile
            remaining_tiles[tile] -= 1

            # Check if this placement is valid
            if is_valid(grid):
                # Recursive call to place the next tile
                result = solve(grid, row, col + 1)
                if result:
                    return result  # Valid solution found

            # Backtrack: Remove the tile and restore its count
            grid[row][col] = '_'
            remaining_tiles[tile] += 1

    return None  # No valid solution found

# Main function to solve the puzzle
def main():
    input_file = "board_config.txt"  # Input file name
    grid = create_grid_from_file(input_file)
    if grid is None:
        return

    print("Initial Grid:")
    for row in grid:
        print(" ".join(row))

    # Solve the puzzle using backtracking
    solution = solve(grid, 0, 0)

    if solution:
        print("\nSolved Grid:")
        for row in solution:
            print(" ".join(row))
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    main()
