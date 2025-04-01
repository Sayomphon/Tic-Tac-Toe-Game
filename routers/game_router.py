# routers/game_router.py
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict # เพิ่ม Dict

# Import game logic and database functions
from game_logic.tictactoe import get_ai_move, check_win_utility, is_board_full_utility
from game_logic import database # Import the database module

router = APIRouter()

# --- Pydantic Models ---

class PlayRequest(BaseModel):
    board: List[str] = Field(..., min_length=9, max_length=9)

class PlayResponse(BaseModel):
    new_board: List[str]
    winner: Optional[str] = None # 'X', 'O', or 'Tie'
    is_tie: bool = False # เพิ่ม field นี้เพื่อให้ชัดเจน
    message: str
    ai_move: Optional[int] = None

class ScoreUpdateRequest(BaseModel):
    player_name: str
    result: str # 'win', 'loss', 'tie'

# โครงสร้างสำหรับข้อมูลผู้เล่นแต่ละคน
class PlayerStats(BaseModel):
    score: int
    win_streak: int
    win_count: int

# ปรับปรุง ScoreResponse ให้ใช้ PlayerStats
class ScoreResponse(BaseModel):
    scores: Dict[str, PlayerStats] # Key เป็นชื่อผู้เล่น, Value เป็น PlayerStats

# --- API Endpoints ---

@router.post("/play", response_model=PlayResponse)
async def play_turn(request: PlayRequest):
    current_board = request.board
    player_mark = 'X'
    ai_mark = 'O'

    # --- (ส่วนตรวจสอบก่อน AI เล่น เหมือนเดิม) ---
    if check_win_utility(current_board, player_mark):
         # Player ชนะก่อน AI เล่น (ไม่น่าเกิดในการเล่นปกติ แต่ใส่ไว้กันเหนียว)
         return PlayResponse(new_board=current_board, winner=player_mark, is_tie=False, message="You win!", ai_move=None)
    if is_board_full_utility(current_board) and not check_win_utility(current_board, player_mark) and not check_win_utility(current_board, ai_mark):
         return PlayResponse(new_board=current_board, winner=None, is_tie=True, message="It's a tie!", ai_move=None)

    # --- Get AI Move ---
    ai_move_index = get_ai_move(current_board, ai_mark) # ควรส่ง mark ของ AI ไปด้วย
    print(f"AI ('{ai_mark}') chooses move: {ai_move_index}")

    new_board = current_board[:]
    winner = None
    is_tie = False
    message = "Error"

    if ai_move_index is not None and new_board[ai_move_index] == "":
        new_board[ai_move_index] = ai_mark

        # --- Check game status after AI move ---
        if check_win_utility(new_board, ai_mark):
            winner = ai_mark
            is_tie = False
            message = "AI (O) wins!"
        elif is_board_full_utility(new_board):
            winner = None # หรือจะให้เป็น "Tie" ก็ได้
            is_tie = True
            message = "It's a tie!"
        else:
            winner = None
            is_tie = False
            message = "AI moved. Your turn."

        return PlayResponse(
            new_board=new_board,
            winner=winner,
            is_tie=is_tie,
            message=message,
            ai_move=ai_move_index
        )
    elif is_board_full_utility(new_board): # กรณี AI ไม่มีที่เดิน และกระดานเต็ม
         return PlayResponse(new_board=new_board, winner=None, is_tie=True, message="Board is full! It's a tie.", ai_move=None)
    else:
         # กรณีเกิดข้อผิดพลาดที่ AI หาช่องเดินไม่ได้ทั้งที่ควรจะมี
         print("Error: AI move index is None or invalid, but board is not full/won.")
         raise HTTPException(status_code=500, detail="Could not determine valid AI move.")


@router.post("/update_score")
async def update_player_score(request: ScoreUpdateRequest):
    """
    Updates a single player's score based on the game result.
    NOTE: Frontend might need to call this twice (once for player, once for bot)
          if using this simple approach.
    """
    try:
        database.update_score(request.player_name, request.result)
        return {"message": f"Score updated for {request.player_name}"}
    except Exception as e:
        print(f"Error updating score for {request.player_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update score for {request.player_name}.")

@router.get("/get_scores", response_model=ScoreResponse)
async def get_all_scores():
    """Retrieves stats (score, win_streak, win_count) for all players."""
    try:
        scores_data = database.get_scores() # ฟังก์ชันนี้ควรคืน Dict[str, Dict[str, int]]
        # ตรวจสอบและแปลงข้อมูลให้ตรงกับ Pydantic Model ถ้าจำเป็น
        # ในกรณีนี้ ถ้า database.get_scores() คืนรูปแบบที่ถูกต้องแล้ว ก็ใช้ได้เลย
        return ScoreResponse(scores=scores_data)
    except Exception as e:
        print(f"Error getting scores: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve scores.")

@router.post("/reset_scores")
async def reset_scores_endpoint(): # เปลี่ยนชื่อเล็กน้อยเพื่อความชัดเจน
    """Resets all player stats to 0."""
    try:
        database.reset_scores()
        return {"message": "Scores have been reset to 0."}
    except Exception as e:
        print(f"Error resetting scores: {e}")
        raise HTTPException(status_code=500, detail=str(e))