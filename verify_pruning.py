import sys
import os

from adversarial_fox_game import GameState, evaluate

def minimax_no_pruning(state, depth, is_maximizing):
    nodes = 1
    
    if state.last_move:
        r, c, tile = state.last_move
        if state.is_fox_after_move(r, c, tile):
            return evaluate(state, depth), nodes
            
    if depth == 0 or not state.get_possible_moves():
        return evaluate(state, depth), nodes

    if is_maximizing:
        v = -float('inf')
        for move in state.get_possible_moves():
            val, count = minimax_no_pruning(state.result(move), depth - 1, False)
            v = max(v, val)
            nodes += count
        return v, nodes
    else:
        v = float('inf')
        for move in state.get_possible_moves():
            val, count = minimax_no_pruning(state.result(move), depth - 1, True)
            v = min(v, val)
            nodes += count
        return v, nodes

def alpha_beta(state, depth, alpha, beta, is_maximizing):
    nodes = 1
    
    if state.last_move:
        r, c, tile = state.last_move
        if state.is_fox_after_move(r, c, tile):
            return evaluate(state, depth), nodes
            
    if depth == 0 or not state.get_possible_moves():
        return evaluate(state, depth), nodes

    if is_maximizing:
        v = -float('inf')
        for move in state.get_possible_moves():
            val, count = alpha_beta(state.result(move), depth - 1, alpha, beta, False)
            v = max(v, val)
            nodes += count
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v, nodes
    else:
        v = float('inf')
        for move in state.get_possible_moves():
            val, count = alpha_beta(state.result(move), depth - 1, alpha, beta, True)
            v = min(v, val)
            nodes += count
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, nodes

def main():
    # 4x4 grid with 4 empty cells
    grid = [
        ["F", "O", "X", "F"],
        ["O", "X", "O", "X"],
        ["X", "O", "F", "O"],
        ["_", "_", "_", "_"]
    ]
    remaining = {"F": 2, "O": 1, "X": 1}
    
    state_minimax = GameState(copy.deepcopy(grid), remaining.copy(), "MAX")
    state_alphabeta = GameState(copy.deepcopy(grid), remaining.copy(), "MAX")
    
    print(f"Initial moves count: {len(state_minimax.get_possible_moves())}")
    
    depth = 4
    
    print(f"Comparing Minimax and Alpha-Beta at depth {depth}...")
    
    _, minimax_nodes = minimax_no_pruning(state_minimax, depth, True)
    print(f"Minimax (no pruning) nodes visited: {minimax_nodes}")
    
    _, ab_nodes = alpha_beta(state_alphabeta, depth, -float('inf'), float('inf'), True)
    print(f"Alpha-Beta pruning nodes visited: {ab_nodes}")
    
    if minimax_nodes > 0:
        reduction = (1 - ab_nodes / minimax_nodes) * 100
        print(f"Reduction in nodes: {reduction:.2f}%")

import copy
if __name__ == "__main__":
    main()
