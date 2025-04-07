# === routers/game_router.py ===
"""REST API endpoints for playing the game and managing player statistics."""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict  # Added Dict for type annotation
from enum import Enum

# Import game logic and database helper functions
from game_logic.tictactoe import (
    get_ai_move,
    check_win_utility,
    is_board_full_utility,
)
from game_logic import database  # Database abstraction layer

router = APIRouter()

# ----------------------------------------------------------------------------
# Data models (Pydantic) ------------------------------------------------------
# ----------------------------------------------------------------------------

class DifficultyLevel(str, Enum):
    """Enumeration of AI difficulty levels supported by the back‑end."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class PlayRequest(BaseModel):
    """Incoming payload when the user makes a move."""

    board: List[str] = Field(..., min_length=9, max_length=9)
    difficulty: DifficultyLevel = DifficultyLevel.EASY  # Default difficulty


class PlayResponse(BaseModel):
    """JSON returned after the AI responds to the user's move."""

    new_board: List[str]
    winner: Optional[str] = None  # 'X', 'O', or None when no winner yet
    is_tie: bool = False
    message: str
    ai_move: Optional[int] = None  # Index (0‑8) chosen by the AI


class ScoreUpdateRequest(BaseModel):
    """Payload used to update the persistent score after each match."""

    player_name: str
    result: str  # one of: 'win', 'loss', 'tie'


class PlayerStats(BaseModel):
    """Statistics stored per player in the database."""

    score: int
    win_streak: int
    win_count: int


class ScoreResponse(BaseModel):
    """Return type for *get_scores* endpoint."""

    scores: Dict[str, PlayerStats]  # Mapping player name → stats


# ----------------------------------------------------------------------------
# Game play endpoint ----------------------------------------------------------
# ----------------------------------------------------------------------------

@router.post("/play", response_model=PlayResponse)
async def play_turn(request: PlayRequest):
    """Process one player turn and let the AI respond.

    The *board* received from the front‑end represents the game state after the
    player has moved.  This function decides the AI move according to the
    requested difficulty level and returns the updated board along with the
    game outcome.
    """

    current_board = request.board
    difficulty = request.difficulty
    player_mark = "X"
    ai_mark = "O"

    # ---------------------------------------------------------------------
    # First, verify whether the game has already ended before the AI moves.
    # ---------------------------------------------------------------------
    if check_win_utility(current_board, player_mark):
        # Player somehow wins before the AI takes a turn (should be rare).
        return PlayResponse(
            new_board=current_board,
            winner=player_mark,
            is_tie=False,
            message="You win!",
            ai_move=None,
        )

    if (
        is_board_full_utility(current_board)
        and not check_win_utility(current_board, player_mark)
        and not check_win_utility(current_board, ai_mark)
    ):
        return PlayResponse(
            new_board=current_board,
            winner=None,
            is_tie=True,
            message="It's a tie!",
            ai_move=None,
        )

    # ---------------------------------------------------------------------
    # Ask the AI to choose a move based on the current board & difficulty.
    # ---------------------------------------------------------------------
    ai_move_index = get_ai_move(current_board, ai_mark, difficulty)

    # Prepare response defaults ------------------------------------------------
    new_board = current_board[:]
    winner = None
    is_tie = False
    message = "Error processing AI move."  # Overwritten later

    if ai_move_index is not None:
        if new_board[ai_move_index] == "":
            # Apply AI move
            new_board[ai_move_index] = ai_mark

            # Evaluate the board state after the AI has moved
            if check_win_utility(new_board, ai_mark):
                winner = ai_mark
                message = "AI (O) wins!"
            elif is_board_full_utility(new_board):
                is_tie = True
                message = "It's a tie!"
            else:
                message = "AI moved. Your turn."
        else:
            # This should never happen – indicates a bug in the AI logic.
            print(f"Error: AI chose occupied square {ai_move_index}")
            raise HTTPException(
                status_code=500, detail="AI logic error: Chose occupied square."
            )

    elif is_board_full_utility(new_board):
        # No possible moves left and *get_ai_move* returned None ⇒ tie.
        is_tie = True
        message = "Board is full! It's a tie."
    else:
        # Unexpected condition – diagnostics help catch bugs early.
        print("Error: get_ai_move returned None, but board doesn't seem finished.")
        raise HTTPException(status_code=500, detail="Could not determine AI move.")

    return PlayResponse(
        new_board=new_board,
        winner=winner,
        is_tie=is_tie,
        message=message,
        ai_move=ai_move_index,
    )


# ----------------------------------------------------------------------------
# Score management endpoints --------------------------------------------------
# ----------------------------------------------------------------------------

@router.post("/update_score")
async def update_player_score(request: ScoreUpdateRequest):
    """Increment or decrement a player's score according to *result*."""

    try:
        database.update_score(request.player_name, request.result)
        return {"message": f"Score updated for {request.player_name}"}
    except Exception as e:
        print(f"Error updating score for {request.player_name}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update score for {request.player_name}."
        )


@router.get("/get_scores", response_model=ScoreResponse)
async def get_all_scores():
    """Return stats (score, win_streak, win_count) for every player."""

    try:
        # *database.get_scores()* should return a dict compatible with ScoreResponse.
        scores_data = database.get_scores()
        return ScoreResponse(scores=scores_data)
    except Exception as e:
        print(f"Error getting scores: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve scores.")


@router.post("/reset_scores")
async def reset_scores_endpoint():
    """Reset all player statistics back to zero (admin function)."""

    try:
        database.reset_scores()
        return {"message": "Scores have been reset to 0."}
    except Exception as e:
        print(f"Error resetting scores: {e}")
        raise HTTPException(status_code=500, detail=str(e))