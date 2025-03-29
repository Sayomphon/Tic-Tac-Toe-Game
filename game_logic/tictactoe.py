# game_logic/tictactoe.py
import random

class TicTacToe:
    def __init__(self):
        self.board = [""] * 9  # Represents the 3x3 board as a flat list
        self.current_winner = None

    def print_board(self):
        # For debugging backend
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))

    def make_move(self, square_index, player_mark):
        if square_index < 0 or square_index >= 9:
             print(f"Error: Square index {square_index} is out of bounds.")
             return False # Invalid index
        if self.board[square_index] == "":
            self.board[square_index] = player_mark
            # Check for winner after making a move
            if self.check_win(player_mark):
                self.current_winner = player_mark
            return True
        print(f"Error: Square {square_index} is already taken.")
        return False # Square already taken

    def check_win(self, player_mark):
        # Check rows, columns, and diagonals
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == player_mark for i in condition):
                return True
        return False

    def is_board_full(self):
        return all(cell != "" for cell in self.board)

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ""]

# --- AI Logic (Placeholder / Simple Random) ---

def get_ai_move(board):
    """
    Placeholder AI: Chooses a random available move.
    Replace this with Minimax later.
    """
    available_moves = [i for i, spot in enumerate(board) if spot == ""]
    if not available_moves:
        return None # No moves left
    return random.choice(available_moves)

# --- Minimax Placeholder ---
def minimax(board, maximizing_player):
    """
    Placeholder for the Minimax algorithm.
    Needs implementation for evaluating board states and recursive calls.
    """
    # TODO: Implement Minimax logic here
    print("Warning: Minimax function not implemented yet.")
    # For now, just return a dummy evaluation score
    if check_win_utility(board, 'O'): # Assuming 'O' is AI
        return {'score': 1}
    elif check_win_utility(board, 'X'): # Assuming 'X' is player
        return {'score': -1}
    elif is_board_full_utility(board):
        return {'score': 0}

    # Placeholder recursive call structure (needs actual logic)
    if maximizing_player:
        max_eval = {'score': -float('inf')}
        # for move in get_available_moves_utility(board):
        #    make_move_temp(...)
        #    evaluation = minimax(new_board, False)
        #    undo_move_temp(...)
        #    if evaluation['score'] > max_eval['score']:
        #        max_eval = evaluation
        return max_eval # Placeholder
    else:
        min_eval = {'score': float('inf')}
        # for move in get_available_moves_utility(board):
        #    make_move_temp(...)
        #    evaluation = minimax(new_board, True)
        #    undo_move_temp(...)
        #    if evaluation['score'] < min_eval['score']:
        #        min_eval = evaluation
        return min_eval # Placeholder


# --- Utility functions needed by Minimax (can be adapted from class methods) ---
def check_win_utility(board, player_mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[i] == player_mark for i in condition):
            return True
    return False

def is_board_full_utility(board):
    return all(cell != "" for cell in board)

def get_available_moves_utility(board):
     return [i for i, spot in enumerate(board) if spot == ""]