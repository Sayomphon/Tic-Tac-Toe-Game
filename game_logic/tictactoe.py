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
"""
def get_ai_move(board, ai_mark):
    available_moves = [i for i, spot in enumerate(board) if spot == ""]
    if not available_moves:
        return None # No moves left
    return random.choice(available_moves)
"""

# ฟังก์ชัน get_ai_move ที่ใช้ Minimax
def get_ai_move(board, ai_mark):
    # 1. หา Mark ของผู้เล่น (คู่ต่อสู้)
    player_mark = 'X' if ai_mark == 'O' else 'O'

    # 2. ตั้งค่าเริ่มต้นสำหรับคะแนนและท่าเดินที่ดีที่สุด
    best_score = -float('inf') # เริ่มด้วยคะแนนต่ำสุดที่เป็นไปได้
    best_move = None

    # 3. หาท่าเดินที่เป็นไปได้ทั้งหมด
    available_moves = get_available_moves_utility(board)

    # ถ้าไม่มีท่าให้เดินแล้ว (ไม่น่าเกิดถ้าเกมดำเนินถูกต้อง)
    if not available_moves:
        return None

    print(f"AI ({ai_mark}) calculating best move using Minimax...")

    # 4. วนลูปพิจารณาทุกท่าเดินที่เป็นไปได้
    for move in available_moves:
        # 4.1 สร้างกระดานจำลอง: สำคัญมากที่ต้อง *คัดลอก* กระดานเดิม
        temp_board = board[:]
        # ลองเดินท่า 'move' นี้บนกระดานจำลอง
        temp_board[move] = ai_mark

        # 4.2 เรียก Minimax เพื่อประเมินผล:
        #    - เราต้องการรู้คะแนน *หลังจาก* AI เดินไปแล้ว
        #    - ตาถัดไปจะเป็นของผู้เล่น (Minimizing Player) ดังนั้น is_maximizing=False
        #    - เริ่มต้น depth ที่ 0
        eval_result = minimax(temp_board, 0, False, player_mark, ai_mark)
        score = eval_result['score'] # ดึงคะแนนจากการประเมิน

        print(f"  - Evaluating move {move}: score = {score}") # สำหรับ Debug

        # 4.3 อัปเดตท่าเดินที่ดีที่สุด:
        #    - ถ้าคะแนนจากการลองเดินท่า 'move' นี้ ดีกว่าคะแนนที่ดีที่สุดที่เคยเจอ
        if score > best_score:
            best_score = score  # อัปเดตคะแนนที่ดีที่สุด
            best_move = move    # อัปเดตท่าเดินที่ดีที่สุด

    # 5. คืนค่าท่าเดินที่ดีที่สุดที่พบ
    print(f"AI ({ai_mark}) chose move {best_move} with best score {best_score}")
    return best_move

# --- Minimax Placeholder ---
"""
def minimax(board, maximizing_player):
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
"""

def minimax(current_board, depth, is_maximizing, player_mark, ai_mark):
    """
    Minimax algorithm implementation for Tic Tac Toe.
    Returns a dictionary like {'score': S, 'move': M} where S is the score and M might be the best move found from this state (optional).
    """
    # --- Base Cases (จุดสิ้นสุดการ Recursion) ---
    if check_win_utility(current_board, ai_mark):
        return {'score': 1} # AI ชนะ (คะแนนสูง)
    elif check_win_utility(current_board, player_mark):
        return {'score': -1} # Player ชนะ (คะแนนต่ำ)
    elif is_board_full_utility(current_board):
        return {'score': 0} # เสมอ (คะแนนกลาง)

    # --- Recursive Steps ---
    if is_maximizing: # ตาของ AI (Maximizer)
        best_score = -float('inf') # เริ่มต้นด้วยคะแนนต่ำสุด
        available_moves = get_available_moves_utility(current_board)

        for move in available_moves:
            # ลองเดินในช่องนั้น
            current_board[move] = ai_mark
            # เรียก minimax สำหรับตาถัดไป (ตาของ Player - Minimizer)
            eval_result = minimax(current_board, depth + 1, False, player_mark, ai_mark)
            # ยกเลิกการเดิน (Backtrack)
            current_board[move] = ""
            # เลือกคะแนนที่ดีที่สุด (สูงสุด)
            best_score = max(best_score, eval_result['score'])
        return {'score': best_score}

    else: # ตาของ Player (Minimizer)
        best_score = float('inf') # เริ่มต้นด้วยคะแนนสูงสุด
        available_moves = get_available_moves_utility(current_board)

        for move in available_moves:
            # ลองเดินในช่องนั้น
            current_board[move] = player_mark
            # เรียก minimax สำหรับตาถัดไป (ตาของ AI - Maximizer)
            eval_result = minimax(current_board, depth + 1, True, player_mark, ai_mark)
            # ยกเลิกการเดิน (Backtrack)
            current_board[move] = ""
            # เลือกคะแนนที่ดีที่สุด (ต่ำสุด) สำหรับ Minimizer
            best_score = min(best_score, eval_result['score'])
        return {'score': best_score}

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