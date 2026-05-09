import copy

class FoxCSP:
    def __init__(self, initial_grid):
        self.rows = 4
        self.cols = 4
        self.variables = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.domains = {v: ['F', 'O', 'X'] for v in self.variables}
        self.max_counts = {'F': 5, 'O': 6, 'X': 5}
        self.assignment = {}
        self.nodes_visited = 0
        
        # Apply initial grid constraints
        for r in range(self.rows):
            for c in range(self.cols):
                val = initial_grid[r][c]
                if val != '_':
                    self.assignment[(r, c)] = val
                    self.domains[(r, c)] = [val]

    def is_consistent(self, var, val, assignment):
        """Checks if assigning val to var is consistent with the current assignment."""
        r, c = var
        # Temporarily add to assignment for check
        temp_assignment = assignment.copy()
        temp_assignment[var] = val
        
        # Check tile counts
        counts = {'F': 0, 'O': 0, 'X': 0}
        for v in temp_assignment.values():
            counts[v] += 1
        for k, v in counts.items():
            if v > self.max_counts[k]:
                return False

        # Helper to get grid value or placeholder
        def get_val(row, col):
            return temp_assignment.get((row, col), '_')

        def contains_invalid(seq):
            if '_' in seq: return False
            return "FOX" in seq or "XOF" in seq

        # Check row
        row_str = "".join([get_val(r, i) for i in range(4)])
        if contains_invalid(row_str): return False
        
        # Check column
        col_str = "".join([get_val(i, c) for i in range(4)])
        if contains_invalid(col_str): return False

        # Check diagonals if applicable
        if r == c:
            diag = "".join([get_val(i, i) for i in range(4)])
            if contains_invalid(diag): return False
        if r + c == 3:
            anti_diag = "".join([get_val(i, 3 - i) for i in range(4)])
            if contains_invalid(anti_diag): return False

        # Check 2x2 subgrid
        sr, sc = (r // 2) * 2, (c // 2) * 2
        subgrid = "".join([get_val(sr, sc), get_val(sr, sc+1), get_val(sr+1, sc), get_val(sr+1, sc+1)])
        if contains_invalid(subgrid): return False

        return True

    def get_mrv_variable(self):
        """Minimum Remaining Values heuristic."""
        unassigned = [v for v in self.variables if v not in self.assignment]
        if not unassigned:
            return None
        # Return variable with smallest domain size
        return min(unassigned, key=lambda v: len(self.domains[v]))

    def forward_check(self, var, val, domains, assignment):
        """Prune domains of unassigned variables based on the new assignment."""
        new_domains = copy.deepcopy(domains)
        
        # Check all unassigned variables
        for neighbor in [v for v in self.variables if v not in assignment]:
            if neighbor == var: continue
            remaining_vals = []
            for n_val in new_domains[neighbor]:
                if self.is_consistent(neighbor, n_val, {**assignment, var: val}):
                    remaining_vals.append(n_val)
            
            if not remaining_vals:
                return None # Failure: domain wiped out
            new_domains[neighbor] = remaining_vals
            
        return new_domains

def backtracking_search(csp):
    return backtrack(csp.assignment, csp.domains, csp)

def backtrack(assignment, domains, csp):
    csp.nodes_visited += 1
    if len(assignment) == len(csp.variables):
        return assignment
    
    var = csp.get_mrv_variable()
    for val in domains[var]:
        if csp.is_consistent(var, val, assignment):
            new_domains = csp.forward_check(var, val, domains, assignment)
            if new_domains is not None:
                assignment[var] = val
                result = backtrack(assignment, new_domains, csp)
                if result is not None:
                    return result
                del assignment[var]
    return None

def load_grid(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().split() for line in f.readlines()]

def print_grid(assignment):
    for r in range(4):
        row = [assignment.get((r, c), '_') for c in range(4)]
        print(" ".join(row))

def main():
    grid = load_grid("board_config.txt")
    print("Initial Grid:")
    for row in grid:
        print(" ".join(row))
    
    csp = FoxCSP(grid)
    solution = backtracking_search(csp)
    
    if solution:
        print("\nSolved Grid (CSP):")
        print_grid(solution)
        print(f"\nNodes visited: {csp.nodes_visited}")
    else:
        print("\nNo solution found.")
        print(f"Nodes visited: {csp.nodes_visited}")

if __name__ == "__main__":
    main()
