# === game_logic/tictactoe.py ===
"""Core game mechanics and AI implementation (Minimax + difficulty tweaks)."""

import random


class TicTacToe:
    """Mutable object that represents a single game instance.

    Although the API primarily uses utility functions operating on *list[str]*
    boards, this class is still useful for manual testing or future extensions.
    """

    def __init__(self):
        # A flat list of nine strings ("", "X", or "O").  Index mapping:
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.board = [""] * 9
        self.current_winner = None

    # ---------------------------------------------------------------------
    # Convenience helpers for local debugging
    # ---------------------------------------------------------------------
    def print_board(self):
        """Pretty‑print the board to stdout – handy while developing."""
        for i in range(0, 9, 3):
            print("|".join(self.board[i : i + 3]))

    def make_move(self, square_index, player_mark):
        """Attempt to mark *square_index* with *player_mark*.

        Returns *True* on success, *False* otherwise.
        """
        if square_index < 0 or square_index >= 9:
            print(f"Error: Square index {square_index} is out of bounds.")
            return False  # Invalid index
        if self.board[square_index] == "":
            self.board[square_index] = player_mark
            # Update winner state after the move
            if self.check_win(player_mark):
                self.current_winner = player_mark
            return True
        print(f"Error: Square {square_index} is already taken.")
        return False  # Square already taken

    def check_win(self, player_mark):
        """Return *True* if *player_mark* currently has three in a row."""
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for condition in win_conditions:
            if all(self.board[i] == player_mark for i in condition):
                return True
        return False

    def is_board_full(self):
        """Return *True* when no empty squares remain."""
        return all(cell != "" for cell in self.board)

    def get_available_moves(self):
        """Return a list of indexes that are still unoccupied."""
        return [i for i, spot in enumerate(self.board) if spot == ""]


# ----------------------------------------------------------------------------
# Functional utilities used by the REST API (stateless)
# ----------------------------------------------------------------------------


def get_ai_move(board, ai_mark, difficulty):
    """Return the index (0‑8) chosen by the AI according to *difficulty*.

    * easy   – always random
    * medium – 50 % chance random, 50 % best move via Minimax
    * hard   – always best move via Minimax
    """

    available_moves = get_available_moves_utility(board)
    if not available_moves:
        return None  # Board is full

    print(f"AI ({ai_mark}) thinking with difficulty: {difficulty}")

    # ------------------------------- EASY ---------------------------------
    if difficulty == "easy":
        print("  - Difficulty: Easy (Choosing random move)")
        return random.choice(available_moves)

    # ------------------------------ MEDIUM --------------------------------
    if difficulty == "medium":
        # 50/50 chance between random and optimal
        if random.random() < 0.5:
            print("  - Difficulty: Medium (Choosing random move by chance)")
            return random.choice(available_moves)
        # Otherwise fall through to the Minimax branch below
        print("  - Difficulty: Medium (Choosing best move via Minimax)")

    # ------------------------------- HARD ---------------------------------
    # Covers both difficulty == "hard" and the 50 % case for "medium" above.
    player_mark = "X" if ai_mark == "O" else "O"
    best_score = -float("inf")
    best_move = None

    print("  - Calculating best move using Minimax...")

    # Shuffle moves so the AI is less predictable when multiple moves have the
    # same score.
    shuffled_moves = available_moves[:]
    random.shuffle(shuffled_moves)

    for move in shuffled_moves:
        temp_board = board[:]
        temp_board[move] = ai_mark
        eval_result = minimax(temp_board, 0, False, player_mark, ai_mark)
        score = eval_result["score"]
        print(f"    - Evaluating move {move}: score = {score}")

        if score > best_score:
            best_score = score
            best_move = move
        elif score == best_score and random.random() < 0.3:
            # Break ties randomly for some variety
            best_move = move

    if best_move is None and available_moves:
        # Fallback that should rarely trigger
        print("Warning: Minimax did not determine a best move. Choosing randomly.")
        best_move = random.choice(available_moves)

    print(f"  - AI ({ai_mark}) chose move {best_move} with best score {best_score}")
    return best_move


# ----------------------------------------------------------------------------
# Minimax implementation ------------------------------------------------------
# ----------------------------------------------------------------------------

def minimax(current_board, depth, is_maximizing, player_mark, ai_mark):
    """Classic Minimax algorithm (no alpha‑beta pruning).

    Returns a *dict* so additional data could be returned in the future without
    changing callers (currently only *score* is used).
    """

    # ------------------------- Base cases --------------------------------
    if check_win_utility(current_board, ai_mark):
        return {"score": 1}  # AI wins
    elif check_win_utility(current_board, player_mark):
        return {"score": -1}  # Player wins
    elif is_board_full_utility(current_board):
        return {"score": 0}  # Tie

    # ----------------------- Recursive step ------------------------------
    if is_maximizing:
        # AI's turn – maximise the score
        best_score = -float("inf")
        for move in get_available_moves_utility(current_board):
            current_board[move] = ai_mark
            eval_result = minimax(current_board, depth + 1, False, player_mark, ai_mark)
            current_board[move] = ""  # Undo move
            best_score = max(best_score, eval_result["score"])
        return {"score": best_score}
    else:
        # Player's turn – minimise the score
        best_score = float("inf")
        for move in get_available_moves_utility(current_board):
            current_board[move] = player_mark
            eval_result = minimax(current_board, depth + 1, True, player_mark, ai_mark)
            current_board[move] = ""  # Undo move
            best_score = min(best_score, eval_result["score"])
        return {"score": best_score}


# ----------------------------------------------------------------------------
# Stand‑alone helper functions ------------------------------------------------
# ----------------------------------------------------------------------------

def check_win_utility(board, player_mark):
    """Stateless version of *TicTacToe.check_win* used by the API."""
    win_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for condition in win_conditions:
        if all(board[i] == player_mark for i in condition):
            return True
    return False


def is_board_full_utility(board):
    """Return *True* when there are no empty strings left in *board*."""
    return all(cell != "" for cell in board)


def get_available_moves_utility(board):
    """Return indexes of empty squares in *board*."""
    return [i for i, spot in enumerate(board) if spot == ""]
