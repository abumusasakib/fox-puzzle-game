import copy

# Initialize tile counts
remaining_tiles = {'F': 5, 'O': 6, 'X': 5}

# Backtracking function to attempt filling the grid
def solve(grid, row, col):
    # Check if we are done
    if row == 4:
        return grid

    # Move to next row if we reach the end of a row
    if col == 4:
        return solve(grid, row + 1, 0)

    # Try placing each tile
    for tile in 'FOX':
        if remaining_tiles[tile] > 0:
            # Place tile and decrease its count
            grid[row][col] = tile
            remaining_tiles[tile] -= 1

            # Check if this placement is valid
            if is_valid(grid, row, col):
                # Recursive call to place the next tile
                result = solve(grid, row, col + 1)
                if result:
                    return result  # Valid solution found

            # Backtrack: remove tile and restore its count
            grid[row][col] = ''
            remaining_tiles[tile] += 1

    return None  # No valid solution found

# Function to check if placing the tile at (row, col) is valid
def is_valid(grid, row, col):
    # Check for "FOX" and "XOF" patterns in rows, columns, and diagonals
    directions = [
        [(0, 1), (0, 2)], [(1, 0), (2, 0)],  # Right and Down
        [(1, 1), (2, 2)], [(1, -1), (2, -2)] # Diagonals
    ]
    for dr, dc in directions:
        if check_pattern(grid, row, col, dr, dc, 'FOX') or check_pattern(grid, row, col, dr, dc, 'XOF'):
            return False
    return True

# Helper function to check patterns in a given direction
def check_pattern(grid, row, col, dr, dc, pattern):
    for i, (r, c) in enumerate([(0, 0), dr, dc]):
        nr, nc = row + r, col + c
        if not (0 <= nr < 4 and 0 <= nc < 4) or grid[nr][nc] != pattern[i]:
            return False
    return True

# Initialize empty grid and solve
empty_grid = [['' for _ in range(4)] for _ in range(4)]
solution = solve(empty_grid, 0, 0)

# Display solution
if solution:
    for row in solution:
        print(" ".join(row))
else:
    print("No solution found.")
