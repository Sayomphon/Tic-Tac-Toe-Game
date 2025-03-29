# routers/game_router.py
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional

# Import game logic and database functions
from game_logic.tictactoe import get_ai_move, check_win_utility, is_board_full_utility
from game_logic import database # Import the database module

router = APIRouter()

# --- Pydantic Models for Request/Response Validation ---

class PlayRequest(BaseModel):
    board: List[str] = Field(..., min_length=9, max_length=9) # Ensure board has 9 elements

class PlayResponse(BaseModel):
    new_board: List[str]
    winner: Optional[str] = None # 'X', 'O', or 'Tie'
    message: str
    ai_move: Optional[int] = None # Index of AI's move

class ScoreUpdateRequest(BaseModel):
    player_name: str = "Player1" # Example default, adjust as needed
    result: str # 'win', 'loss', 'tie'

class ScoreResponse(BaseModel):
    scores: dict

# --- API Endpoints ---

@router.post("/play", response_model=PlayResponse)
async def play_turn(request: PlayRequest):
    """
    Handles a player's move and returns the AI's response.
    """
    current_board = request.board
    player_mark = 'X'
    ai_mark = 'O'

    print(f"Received board: {current_board}")

    # Basic validation (ensure it's not already won/full before AI moves)
    if check_win_utility(current_board, player_mark):
         return PlayResponse(new_board=current_board, winner=player_mark, message="Player X already won!")
    if check_win_utility(current_board, ai_mark):
         return PlayResponse(new_board=current_board, winner=ai_mark, message="Player O already won!")
    if is_board_full_utility(current_board):
        return PlayResponse(new_board=current_board, winner="Tie", message="Board is full! It's a tie.")

    # --- Get AI Move (Simple random for now) ---
    ai_move_index = get_ai_move(current_board)
    print(f"AI chooses move: {ai_move_index}")

    new_board = current_board[:] # Create a copy

    if ai_move_index is not None:
        if new_board[ai_move_index] == "":
            new_board[ai_move_index] = ai_mark
        else:
            # This case shouldn't happen if get_ai_move is correct
             print("Error: AI tried to move on an occupied square.")
             raise HTTPException(status_code=500, detail="AI logic error.")

        # --- Check game status after AI move ---
        if check_win_utility(new_board, ai_mark):
            winner = ai_mark
            message = "AI (O) wins!"
        elif is_board_full_utility(new_board):
            winner = "Tie"
            message = "It's a tie!"
        else:
            winner = None
            message = "AI moved. Your turn."

        return PlayResponse(new_board=new_board, winner=winner, message=message, ai_move=ai_move_index)
    else:
        # No moves left, but wasn't detected as full before? Should be caught earlier.
        if is_board_full_utility(new_board) and not check_win_utility(new_board, player_mark) and not check_win_utility(new_board, ai_mark):
             return PlayResponse(new_board=new_board, winner="Tie", message="Board is full! It's a tie.")
        else:
             # This might indicate an issue if it's reached when moves are expected
             print("Error: No AI move generated, but board state seems playable.")
             raise HTTPException(status_code=500, detail="Could not determine AI move.")


@router.post("/update_score")
async def update_player_score(request: ScoreUpdateRequest):
    """Updates the player's score based on the game result."""
    try:
        # Use the function from the database module
        database.update_score(request.player_name, request.result)
        return {"message": f"Score updated for {request.player_name}"}
    except Exception as e:
        # Log the error ideally
        print(f"Error updating score: {e}")
        raise HTTPException(status_code=500, detail="Failed to update score.")

@router.get("/get_scores", response_model=ScoreResponse)
async def get_all_scores():
    """Retrieves scores for all players."""
    try:
        # Use the function from the database module
        scores_data = database.get_scores()
        return ScoreResponse(scores=scores_data)
    except Exception as e:
        # Log the error ideally
        print(f"Error getting scores: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve scores.")