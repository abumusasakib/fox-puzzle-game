import copy
import os

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
        
        # Precompute neighbors (variables that share a constraint)
        self.neighbors = {v: set() for v in self.variables}
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2: continue
                r1, c1 = v1
                r2, c2 = v2
                # Same row, col, or diagonal
                if r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2):
                    self.neighbors[v1].add(v2)
                # Same 2x2 subgrid
                elif (r1//2 == r2//2) and (c1//2 == c2//2):
                    self.neighbors[v1].add(v2)

    def is_consistent(self, var, val, assignment):
        """Checks if assigning val to var is consistent with the current assignment."""
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
            # Check for "FOX" or "XOF" in full or partial sequences
            if "FOX" in seq or "XOF" in seq: return True
            return False

        r, c = var
        # Check row
        if contains_invalid("".join([get_val(r, i) for i in range(4)])): return False
        # Check column
        if contains_invalid("".join([get_val(i, c) for i in range(4)])): return False
        
        # Check all diagonals passing through (r,c)
        diag1 = []
        for i in range(-3, 4):
            nr, nc = r + i, c + i
            if 0 <= nr < 4 and 0 <= nc < 4: diag1.append(get_val(nr, nc))
        if contains_invalid("".join(diag1)): return False
        
        diag2 = []
        for i in range(-3, 4):
            nr, nc = r + i, c - i
            if 0 <= nr < 4 and 0 <= nc < 4: diag2.append(get_val(nr, nc))
        if contains_invalid("".join(diag2)): return False

        # Check 2x2 subgrid
        sr, sc = (r // 2) * 2, (c // 2) * 2
        subgrid = "".join([get_val(sr, sc), get_val(sr, sc+1), get_val(sr+1, sc), get_val(sr+1, sc+1)])
        if contains_invalid(subgrid): return False

        return True

    def get_mrv_variable(self, assignment, domains):
        """Minimum Remaining Values heuristic."""
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned: return None
        return min(unassigned, key=lambda v: len(domains[v]))

    def ac3(self, domains, assignment, queue=None):
        """Arc Consistency algorithm (AC-3)."""
        if queue is None:
            queue = []
            for v1 in self.variables:
                for v2 in self.neighbors[v1]:
                    queue.append((v1, v2))
        
        while queue:
            (Xi, Xj) = queue.pop(0)
            if self.revise(Xi, Xj, domains, assignment):
                if not domains[Xi]:
                    return False # Domain wiped out
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def revise(self, Xi, Xj, domains, assignment):
        """Updates domain of Xi to be consistent with Xj."""
        revised = False
        for x in domains[Xi][:]:
            # Check if there exists ANY value y in Dj that is consistent with Xi=x
            # given current assignment
            has_support = False
            for y in domains[Xj]:
                if self.is_consistent(Xi, x, {**assignment, Xj: y}):
                    has_support = True
                    break
            if not has_support:
                domains[Xi].remove(x)
                revised = True
        return revised

def backtracking_search(csp):
    # Initial AC-3
    csp.ac3(csp.domains, csp.assignment)
    return backtrack(csp.assignment, csp.domains, csp)

def backtrack(assignment, domains, csp):
    csp.nodes_visited += 1
    if len(assignment) == len(csp.variables):
        return assignment
    
    var = csp.get_mrv_variable(assignment, domains)
    for val in domains[var]:
        if csp.is_consistent(var, val, assignment):
            # Maintaining Arc Consistency (MAC)
            new_assignment = {**assignment, var: val}
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [val]
            
            # Queue for AC-3: arcs pointing TO unassigned neighbors of var
            queue = [(Xk, var) for Xk in csp.neighbors[var] if Xk not in new_assignment]
            
            if csp.ac3(new_domains, new_assignment, queue):
                result = backtrack(new_assignment, new_domains, csp)
                if result is not None:
                    return result
    return None

def load_grid(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().split() for line in f.readlines()]

def print_grid(assignment):
    for r in range(4):
        row = [assignment.get((r, c), '_') for c in range(4)]
        print(" ".join(row))

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "board_config.txt")
    
    grid = load_grid(config_path)
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
