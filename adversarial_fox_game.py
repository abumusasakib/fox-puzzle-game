import tkinter as tk
from tkinter import messagebox
import random
import copy
import time

# --- AI Logic ---

class GameState:
    def __init__(self, grid=None, remaining_tiles=None, turn="MAX"):
        self.grid = grid if grid else [["_" for _ in range(4)] for _ in range(4)]
        self.remaining_tiles = remaining_tiles if remaining_tiles else {"F": 5, "O": 6, "X": 5}
        self.turn = turn
        self.last_move = None

    def get_possible_moves(self):
        moves = []
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == "_":
                    for tile, count in self.remaining_tiles.items():
                        if count > 0:
                            moves.append((r, c, tile))
        return moves

    def is_fox_after_move(self, row, col, tile):
        temp_grid = [r[:] for r in self.grid]
        temp_grid[row][col] = tile
        
        def contains_fox(seq):
            return "FOX" in seq or "XOF" in seq

        # 1. Check row
        if contains_fox("".join(temp_grid[row])): return True
        
        # 2. Check col
        if contains_fox("".join([temp_grid[i][col] for i in range(4)])): return True
        
        # 3. Check diagonal (top-left to bottom-right)
        # The diagonal is defined by r - c = constant
        diag1 = []
        for i in range(-3, 4):
            r, c = row + i, col + i
            if 0 <= r < 4 and 0 <= c < 4:
                diag1.append(temp_grid[r][c])
        if contains_fox("".join(diag1)): return True
        
        # 4. Check anti-diagonal (top-right to bottom-left)
        # The anti-diagonal is defined by r + c = constant
        diag2 = []
        for i in range(-3, 4):
            r, c = row + i, col - i
            if 0 <= r < 4 and 0 <= c < 4:
                diag2.append(temp_grid[r][c])
        if contains_fox("".join(diag2)): return True
        
        # 5. Check 2x2 subgrid
        sr, sc = (row // 2) * 2, (col // 2) * 2
        subgrid = "".join([temp_grid[sr][sc], temp_grid[sr][sc+1], temp_grid[sr+1][sc], temp_grid[sr+1][sc+1]])
        if contains_fox(subgrid): return True

        return False

    def result(self, move):
        r, c, tile = move
        new_grid = [row[:] for row in self.grid]
        new_grid[r][c] = tile
        new_tiles = self.remaining_tiles.copy()
        new_tiles[tile] -= 1
        new_turn = "MIN" if self.turn == "MAX" else "MAX"
        new_state = GameState(new_grid, new_tiles, new_turn)
        new_state.last_move = move
        return new_state

def evaluate(state, depth):
    if state.last_move:
        r, c, tile = state.last_move
        if state.is_fox_after_move(r, c, tile):
            return -1000 - depth if state.turn == "MIN" else 1000 + depth
    return 0

def alpha_beta(state, depth, alpha, beta, is_maximizing):
    if state.last_move:
        r, c, tile = state.last_move
        if state.is_fox_after_move(r, c, tile):
            return evaluate(state, depth)
            
    if depth == 0 or not state.get_possible_moves():
        return evaluate(state, depth)

    if is_maximizing:
        v = -float('inf')
        for move in state.get_possible_moves():
            v = max(v, alpha_beta(state.result(move), depth - 1, alpha, beta, False))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float('inf')
        for move in state.get_possible_moves():
            v = min(v, alpha_beta(state.result(move), depth - 1, alpha, beta, True))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

def get_best_move(state, depth):
    moves = state.get_possible_moves()
    safe_moves = [m for m in moves if not state.is_fox_after_move(m[0], m[1], m[2])]
    if not safe_moves: return moves[0] if moves else None
    
    best_move = None
    best_val = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    for move in safe_moves:
        val = alpha_beta(state.result(move), depth - 1, alpha, beta, False)
        if val > best_val:
            best_val = val
            best_move = move
        alpha = max(alpha, best_val)
    return best_move

# --- GUI Implementation ---

class AdversarialFoxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Competitive FOX Game (AI vs Human)")
        self.root.geometry("450x750")
        self.root.configure(bg="#f0f0f0")
        
        self.state = GameState(turn="MIN")
        self.selected_tile = tk.StringVar(value="F")
        self.buttons = []
        self.depth = 3 # AI depth
        
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Competitive FOX Game", font=("Arial", 20, "bold"), bg="#f0f0f0", pady=10).pack()
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0")
        status_frame.pack(pady=5)
        
        self.turn_label = tk.Label(status_frame, text="Your Turn", font=("Arial", 14), bg="#f0f0f0")
        self.turn_label.pack()
        
        self.count_label = tk.Label(status_frame, text="", font=("Arial", 12), bg="#f0f0f0")
        self.count_label.pack()

        # Grid Frame
        grid_frame = tk.Frame(self.root, bg="#d0d0d0", bd=2, relief="sunken")
        grid_frame.pack(pady=10)
        
        for r in range(4):
            row_btns = []
            for c in range(4):
                btn = tk.Button(grid_frame, text="", width=4, height=2, font=("Arial", 18, "bold"),
                                command=lambda r=r, c=c: self.on_cell_click(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(btn)
            self.buttons.append(row_btns)

        # Tile Palette
        palette_frame = tk.LabelFrame(self.root, text="Select Tile to Place", font=("Arial", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        palette_frame.pack(pady=10)
        
        for t in ["F", "O", "X"]:
            tk.Radiobutton(palette_frame, text=f"Tile {t}", variable=self.selected_tile, value=t, 
                           font=("Arial", 12), bg="#f0f0f0", indicatoron=0, width=8, selectcolor="#add8e6").pack(side="left", padx=5)

        # Controls
        ctrl_frame = tk.Frame(self.root, bg="#f0f0f0")
        ctrl_frame.pack(pady=20)
        
        tk.Button(ctrl_frame, text="Reset Game", font=("Arial", 12), command=self.reset_game, width=15).pack(pady=5)
        tk.Button(ctrl_frame, text="Rules", font=("Arial", 12), command=self.show_rules, width=15).pack(pady=5)

    def on_cell_click(self, r, c):
        if self.state.turn != "MIN" or self.state.grid[r][c] != "_":
            return
        
        tile = self.selected_tile.get()
        if self.state.remaining_tiles[tile] <= 0:
            messagebox.showwarning("Out of Tiles", f"No more {tile} tiles left!")
            return
        
        # Player Move
        move = (r, c, tile)
        is_losing = self.state.is_fox_after_move(r, c, tile)
        self.state = self.state.result(move)
        self.update_ui()
        
        if is_losing:
            self.game_over("AI (MAX) Wins! You created a FOX.")
            return

        if not self.state.get_possible_moves():
            self.game_over("Draw! Grid is full.")
            return

        # AI Turn
        self.root.after(500, self.ai_turn)

    def ai_turn(self):
        self.turn_label.config(text="AI is thinking...", fg="red")
        self.root.update()
        
        move = get_best_move(self.state, self.depth)
        if not move:
            self.game_over("Draw! No moves left.")
            return
            
        r, c, tile = move
        is_losing = self.state.is_fox_after_move(r, c, tile)
        self.state = self.state.result(move)
        self.update_ui()
        
        if is_losing:
            self.game_over("You (MIN) Win! AI created a FOX.")
            return
            
        if not self.state.get_possible_moves():
            self.game_over("Draw! Grid is full.")
            return
            
        self.turn_label.config(text="Your Turn", fg="blue")

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                val = self.state.grid[r][c]
                self.buttons[r][c].config(text=val if val != "_" else "", state="normal" if val == "_" else "disabled")
                if val == "F": self.buttons[r][c].config(disabledforeground="blue")
                elif val == "O": self.buttons[r][c].config(disabledforeground="green")
                elif val == "X": self.buttons[r][c].config(disabledforeground="red")
        
        counts = self.state.remaining_tiles
        self.count_label.config(text=f"F: {counts['F']}  |  O: {counts['O']}  |  X: {counts['X']}")

    def reset_game(self):
        self.state = GameState(turn="MIN")
        self.update_ui()
        self.turn_label.config(text="Your Turn", fg="blue")

    def game_over(self, msg):
        messagebox.showinfo("Game Over", msg)
        self.reset_game()

    def show_rules(self):
        rules = (
            "1. Two players: You (MIN) and AI (MAX).\n"
            "2. Take turns placing a tile (F, O, or X).\n"
            "3. Goal: AVOID completing the word 'FOX' or 'XOF'.\n"
            "4. Direction: Horizontal, vertical, or diagonal.\n"
            "5. Subgrids: 2x2 blocks are also checked.\n"
            "6. Lose: The player who completes a FOX loses immediately!"
        )
        messagebox.showinfo("Game Rules", rules)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdversarialFoxGUI(root)
    root.mainloop()
