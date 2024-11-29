def create_grid_from_file(file_path):
    """
    Reads a 4x4 board configuration from a file.
    """
    try:
        with open(file_path, "r") as file:
            grid = [line.strip().split() for line in file.readlines()]
        print("Parsed Grid:")
        for row in grid:
            print(" ".join(row))
        # Validate grid dimensions
        if len(grid) != 4 or any(len(row) != 4 for row in grid):
            raise ValueError("The grid must be a 4x4 configuration.")
        return grid
    except Exception as e:
        print(f"Error reading grid: {e}")
        return None


def is_valid(grid, row, col, tile):
    """
    Checks if placing a tile at (row, col) is valid.
    """
    grid[row][col] = tile  # Temporarily place the tile

    # Helper function to check for invalid patterns
    def contains_invalid(seq):
        if "_" in seq:
            return False
        return "FOX" in seq or "XOF" in seq

    # Check row and column
    row_str = "".join(grid[row])
    col_str = "".join([grid[i][col] for i in range(4)])
    if contains_invalid(row_str) or contains_invalid(col_str):
        grid[row][col] = "_"  # Undo placement
        return False

    # Check diagonals
    if row == col:  # Main diagonal
        diag = "".join([grid[i][i] for i in range(4)])
        if contains_invalid(diag):
            grid[row][col] = "_"  # Undo placement
            return False
    if row + col == 3:  # Anti-diagonal
        anti_diag = "".join([grid[i][3 - i] for i in range(4)])
        if contains_invalid(anti_diag):
            grid[row][col] = "_"  # Undo placement
            return False

    # Check 2x2 subgrid
    start_row, start_col = row // 2 * 2, col // 2 * 2
    subgrid = [
        grid[start_row][start_col],
        grid[start_row][start_col + 1],
        grid[start_row + 1][start_col],
        grid[start_row + 1][start_col + 1],
    ]
    subgrid_str = "".join(subgrid)
    if contains_invalid(subgrid_str):
        grid[row][col] = "_"  # Undo placement
        return False

    grid[row][col] = "_"  # Undo placement
    return True


def solve_grid(grid, row=0, col=0, remaining_tiles=None):
    """
    Backtracking solver to complete the grid.
    """
    if remaining_tiles is None:
        # Count remaining tiles
        remaining_tiles = {"F": 5, "O": 6, "X": 5}
        for r in grid:
            for t in r:
                if t in remaining_tiles:
                    remaining_tiles[t] -= 1

    # If we've reached the end of the grid, the puzzle is solved
    if row == 4:
        return True

    # Calculate next cell
    next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)

    # If the current cell is pre-filled, move to the next cell
    if grid[row][col] != "_":
        return solve_grid(grid, next_row, next_col, remaining_tiles)

    # Try placing each available tile
    for tile, count in remaining_tiles.items():
        if count > 0 and is_valid(grid, row, col, tile):
            grid[row][col] = tile
            remaining_tiles[tile] -= 1

            if solve_grid(grid, next_row, next_col, remaining_tiles):
                return True

            # Backtrack
            grid[row][col] = "_"
            remaining_tiles[tile] += 1

    return False


def main():
    input_file = "board_config.txt"  # Input file name
    grid = create_grid_from_file(input_file)
    if grid is None:
        return

    print("Initial Grid:")
    for row in grid:
        print(" ".join(row))

    if solve_grid(grid):
        print("\nSolved Grid:")
        for row in grid:
            print(" ".join(row))
    else:
        print("\nNo solution could be found.")


if __name__ == "__main__":
    main()
