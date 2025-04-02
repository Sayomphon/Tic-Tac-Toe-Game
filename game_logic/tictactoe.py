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

# **** แก้ไข get_ai_move ให้รับ difficulty และเปลี่ยน Logic ****
def get_ai_move(board, ai_mark, difficulty): # รับ difficulty เพิ่ม
    available_moves = get_available_moves_utility(board)
    if not available_moves:
        return None

    print(f"AI ({ai_mark}) thinking with difficulty: {difficulty}")

    # --- Logic เลือกท่าเดินตาม Difficulty ---
    if difficulty == "easy":
        # EASY: เลือกท่าเดินแบบสุ่มเสมอ
        print("  - Difficulty: Easy (Choosing random move)")
        return random.choice(available_moves)

    elif difficulty == "medium":
        # MEDIUM: มีโอกาส 50% ที่จะเดินสุ่ม, 50% ที่จะเดินแบบ Minimax
        if random.random() < 0.5: # random.random() ให้ค่า float ระหว่าง 0.0 ถึง 1.0
            print("  - Difficulty: Medium (Choosing random move by chance)")
            return random.choice(available_moves)
        else:
            print("  - Difficulty: Medium (Choosing best move via Minimax)")
            # ถ้าไม่สุ่ม ก็จะไปใช้ Logic ของ Hard (Minimax) ด้านล่าง
            pass # ใช้ pass เพื่อให้โค้ดไหลลงไปที่ส่วน Hard

    # HARD (หรือ Medium ที่ไม่สุ่ม): ใช้ Minimax
    # (เงื่อนไขครอบคลุม difficulty == "hard" หรือกรณีที่มาจาก medium แล้วไม่สุ่ม)
    if difficulty == "hard" or difficulty == "medium":
         player_mark = 'X' if ai_mark == 'O' else 'O'
         best_score = -float('inf')
         best_move = None

         print(f"  - Calculating best move using Minimax...")

         # สร้าง List ของท่าเดินที่เป็นไปได้ (อาจจะสลับลำดับเพื่อความไม่แน่นอนเล็กน้อย ถ้าต้องการ)
         shuffled_moves = available_moves[:] # ทำสำเนา
         random.shuffle(shuffled_moves) # สลับลำดับท่าเดินที่จะพิจารณา

         for move in shuffled_moves: # วนลูปตามลำดับที่สลับแล้ว
             temp_board = board[:]
             temp_board[move] = ai_mark
             eval_result = minimax(temp_board, 0, False, player_mark, ai_mark)
             score = eval_result['score']
             print(f"    - Evaluating move {move}: score = {score}")

             # อัปเดตท่าที่ดีที่สุด
             # (อาจจะเก็บท่าทั้งหมดที่มีคะแนนเท่ากัน แล้วสุ่มเลือกตอนท้าย เพื่อให้ Hard ดูไม่ตายตัวเกินไป)
             if score > best_score:
                 best_score = score
                 best_move = move
             # Optional: ถ้าคะแนนเท่ากัน ให้มีโอกาสเปลี่ยน best_move บ้างเล็กน้อย
             elif score == best_score:
                 if random.random() < 0.3: # โอกาส 30% ที่จะเปลี่ยนไปใช้ท่าใหม่ที่คะแนนเท่าเดิม
                     best_move = move


         # กรณีที่ไม่ควรเกิด: ถ้าวนลูปแล้วยังไม่ได้ best_move (อาจเกิดถ้ามี bug ใน minimax หรือ available_moves)
         if best_move is None and available_moves:
             print("Warning: Minimax did not determine a best move. Choosing randomly.")
             best_move = random.choice(available_moves) # เลือกสุ่มเป็น Fallback

         print(f"  - AI ({ai_mark}) chose move {best_move} with best score {best_score}")
         return best_move

    else:
        # กรณีค่า difficulty ไม่รู้จัก (ไม่ควรเกิดถ้า Frontend/Backend ทำงานถูกต้อง)
        print(f"Warning: Unknown difficulty '{difficulty}'. Defaulting to random move.")
        return random.choice(available_moves)

# --- Minimax Placeholder ---

def minimax(current_board, depth, is_maximizing, player_mark, ai_mark):
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