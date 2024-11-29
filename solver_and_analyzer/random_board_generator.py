import random

def create_grid():
    # Define the letter counts
    letters = ['F'] * 5 + ['O'] * 6 + ['X'] * 5
    random.shuffle(letters)
    return [letters[i:i+4] for i in range(0, 16, 4)]

def check_no_fox(grid):
    # Check rows and columns
    for i in range(4):
        row = "".join(grid[i])
        col = "".join([grid[j][i] for j in range(4)])
        if "FOX" in row or "FOX" in col or "XOF" in row or "XOF" in col:
            return False
    
    # Check diagonals
    diagonals = [
        "".join([grid[i][i] for i in range(4)]),
        "".join([grid[i][3-i] for i in range(4)])
    ]
    for diag in diagonals:
        if "FOX" in diag or "XOF" in diag:
            return False

    # Check 2x2 subgrids for "FOX" or "XOF" patterns
    for i in range(3):
        for j in range(3):
            square = [
                grid[i][j], grid[i][j+1],
                grid[i+1][j], grid[i+1][j+1]
            ]
            square_str = "".join(square)
            if "FOX" in square_str or "XOF" in square_str:
                return False

    return True

def find_valid_grid():
    while True:
        grid = create_grid()
        if check_no_fox(grid):
            return grid

# Run the function and display the result
grid = find_valid_grid()
for row in grid:
    print(" ".join(row))