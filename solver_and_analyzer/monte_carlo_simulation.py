import random
from math import factorial

"""
Insights about the game:

1. **High Proportion of Invalid Configurations**:
   - The estimated **proportion of invalid configurations** is approximately **84.10%**. This means that the majority of random 4x4 arrangements of 5 "F"s, 6 "O"s, and 5 "X"s will contain the forbidden sequence "FOX" or "XOF" in some direction.
   - This high percentage shows that the constraint is quite restrictive, making it challenging to find valid configurations without encountering "FOX."

2. **Relatively Low Proportion of Valid Configurations**:
   - The **proportion of valid configurations** is around **15.90%**, meaning only about 16 out of every 100 random arrangements will meet the game's requirements.
   - Although the restriction is significant, there are still enough valid configurations, given the total possible configurations (over 200,000 valid configurations).

3. **Total Solution Space**:
   - With a **total of 2,018,016 possible configurations**, an estimated **320,770 configurations** are valid.
   - This means there are likely hundreds of thousands of ways to arrange the tiles that meet the game's rules, so finding a solution is feasible.

4. **Inference for Game Design or Strategy**:
   - Given the high percentage of invalid configurations, a random placement strategy is not efficient for finding a solution. A systematic or guided approach (e.g., avoiding placements that lead to "FO" patterns early on) might be more practical.
   - Despite the constraints, the large number of valid configurations suggests the puzzle has flexibility, with multiple solutions possible.

### Summary
- **84.10% of configurations** contain the forbidden "FOX" sequence, making them invalid.
- **15.90% of configurations** are valid, meaning there are many potential solutions, but finding one randomly may take several attempts.
- **2,018,016 total configurations** are possible, but only **320,770** are valid.

This information is useful for understanding the game's difficulty and the balance between constraints and possible solutions.
"""

# Function to calculate multinomial coefficient for total configurations
def total_configurations():
    return factorial(16) // (factorial(5) * factorial(6) * factorial(5))

# Generate a random 4x4 grid with 5 'F's, 6 'O's, and 5 'X's
def create_random_grid():
    letters = ['F'] * 5 + ['O'] * 6 + ['X'] * 5
    random.shuffle(letters)
    return [letters[i:i+4] for i in range(0, 16, 4)]

# Check if the grid contains "FOX" or "XOF" in any row, column, or diagonal
def contains_fox(grid):
    # Check rows and columns
    for i in range(4):
        row = "".join(grid[i])
        col = "".join([grid[j][i] for j in range(4)])
        if "FOX" in row or "FOX" in col or "XOF" in row or "XOF" in col:
            return True
    
    # Check diagonals
    diagonals = [
        "".join([grid[i][i] for i in range(4)]),
        "".join([grid[i][3-i] for i in range(4)])
    ]
    for diag in diagonals:
        if "FOX" in diag or "XOF" in diag:
            return True

    return False

# Monte Carlo Simulation to estimate the number of invalid configurations
def monte_carlo_simulation(num_samples):
    invalid_count = 0
    
    for _ in range(num_samples):
        grid = create_random_grid()
        if contains_fox(grid):
            invalid_count += 1

    # Calculate the proportion of invalid configurations
    invalid_ratio = invalid_count / num_samples
    
    # Estimate total invalid configurations in the solution space
    total_invalid = int(total_configurations() * invalid_ratio)
    total_valid = total_configurations() - total_invalid
    
    return total_invalid, total_valid

# Running the simulation
num_samples = 1000000  # Sample size for Monte Carlo simulation
total_invalid, total_valid = monte_carlo_simulation(num_samples)

print(f"Estimated Number of Invalid Configurations: {total_invalid}")
print(f"Estimated Number of Valid Configurations: {total_valid}")
print(f"Total Configurations: {total_configurations()}")
print(f"Proportion of Invalid Configurations: {total_invalid / total_configurations():.4f}")
print(f"Proportion of Valid Configurations: {total_valid / total_configurations():.4f}")
