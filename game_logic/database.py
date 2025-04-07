import sqlite3
import os
from typing import Dict, Any

# --- Configuration ---
# Construct the path to the SQLite database file (tic_tac_toe.db) 
# based on the current directory of this Python file.
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'db', 'tic_tac_toe.db')

# --- Dummy Data (Enhanced to store win_count) ---
# Use a dictionary to simulate the DB structure for now:
# { player_name: {"score": int, "win_streak": int, "win_count": int} }
_player_stats: Dict[str, Dict[str, int]] = {
    "Player1": {"score": 0, "win_streak": 0, "win_count": 0},
    "Bot": {"score": 0, "win_streak": 0, "win_count": 0}  # Added a default Bot entry as well
}

def initialize_database():
    """
    Checks if the required database and table exist.
    Creates them if not found.
    This function is automatically called once when the module is imported.
    """
    try:
        # Ensure the directory for the database file exists.
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to the database and create cursor.
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create 'scores' table if it doesn't exist, ensuring columns for
        # score, win_streak, and win_count are present.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT UNIQUE NOT NULL,
                score INTEGER DEFAULT 0,
                win_streak INTEGER DEFAULT 0,
                win_count INTEGER DEFAULT 0
            )
        ''')
        
        # Insert default player rows if they do not exist,
        # so we always have at least 'Player1' and 'Bot'.
        cursor.execute("INSERT OR IGNORE INTO scores (player_name) VALUES (?)", ("Player1",))
        cursor.execute("INSERT OR IGNORE INTO scores (player_name) VALUES (?)", ("Bot",))
        
        conn.commit()
        conn.close()
        print(f"Database initialized/checked at: {db_path}")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during DB initialization: {e}")

def _ensure_player_exists(player_name: str):
    """
    Helper function to ensure that the given player_name 
    exists in the dummy data dictionary. If not, 
    a new record is created with default stats.
    """
    global _player_stats
    if player_name not in _player_stats:
        _player_stats[player_name] = {"score": 0, "win_streak": 0, "win_count": 0}
        print(f"Initialized dummy stats for {player_name}")

def update_score(player_name: str, result: str):
    """
    Updates the player's stats in the dummy dictionary 
    based on the game result. Possible results are:
    - 'win': increment score, increment win_count, adjust win_streak 
    - 'loss': decrement score, reset win_streak 
    - 'tie': reset win_streak
    If the player's win_streak hits 3, an additional bonus point is given
    and the win_streak is reset to 0.

    NOTE: The commented-out section is the intended code for an actual SQLite DB.
    Right now, it is replaced by an in-memory dictionary for demonstration.
    """
    global _player_stats
    _ensure_player_exists(player_name)  # Check if the player is in the dummy data

    stats = _player_stats[player_name]

    if result == "win":
        stats["score"] += 1
        stats["win_count"] += 1  # Increase total wins
        stats["win_streak"] += 1
        if stats["win_streak"] == 3:
            print(f"{player_name} got a 3-win streak bonus!")
            stats["score"] += 1   # Bonus point for 3-win streak
            stats["win_streak"] = 0  # Reset the streak
    elif result == "loss":
        stats["score"] -= 1
        stats["win_streak"] = 0  # Reset streak on loss
    elif result == "tie":
        stats["win_streak"] = 0  # Reset streak on tie

    print(f"Updated stats for {player_name}: Score={stats['score']}, Streak={stats['win_streak']}, Wins={stats['win_count']}")

    # --- TODO: Replace the dummy logic above with actual SQLite update logic ---
    # The commented-out code below demonstrates how to handle real DB operations.

    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # try:
    #     # Fetch current stats from the DB.
    #     cursor.execute("SELECT score, win_streak, win_count FROM scores WHERE player_name = ?", (player_name,))
    #     row = cursor.fetchone()
    #
    #     if not row:
    #         # If there's no entry for this player, insert a new one.
    #         cursor.execute("INSERT INTO scores (player_name, score, win_streak, win_count) VALUES (?, 0, 0, 0)", (player_name,))
    #         current_score, current_streak, current_wins = 0, 0, 0
    #     else:
    #         current_score, current_streak, current_wins = row
    #
    #     # Calculate new stats based on the result.
    #     new_score = current_score
    #     new_streak = current_streak
    #     new_wins = current_wins
    #
    #     if result == "win":
    #         new_score += 1
    #         new_wins += 1
    #         new_streak += 1
    #         if new_streak == 3:
    #             new_score += 1  # Bonus
    #             new_streak = 0
    #     elif result == "loss":
    #         new_score -= 1
    #         new_streak = 0
    #     elif result == "tie":
    #         new_streak = 0
    #
    #     # Update the record in the DB.
    #     cursor.execute("""
    #         UPDATE scores
    #         SET score = ?, win_streak = ?, win_count = ?
    #         WHERE player_name = ?
    #     """, (new_score, new_streak, new_wins, player_name))
    #
    #     conn.commit()
    # except sqlite3.Error as e:
    #     print(f"Database error updating score for {player_name}: {e}")
    # finally:
    #     conn.close()

def reset_scores():
    """
    Resets all stats (score, win_streak, win_count) for all players 
    in the dummy data dictionary to 0.
    
    NOTE: Replace with actual SQLite update if you want to persist 
    resets in the real database.
    """
    global _player_stats
    for player in _player_stats:
        _player_stats[player] = {"score": 0, "win_streak": 0, "win_count": 0}
    print("Dummy scores have been reset.")

    # --- TODO: Replace/Add actual SQLite update for resetting all scores ---
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # try:
    #     cursor.execute("UPDATE scores SET score = 0, win_streak = 0, win_count = 0")
    #     conn.commit()
    #     print("Database scores have been reset.")
    # except sqlite3.Error as e:
    #     print(f"Database error resetting scores: {e}")
    # finally:
    #     conn.close()

def get_scores() -> Dict[str, Dict[str, int]]:
    """
    Retrieves the dummy data for all player stats (score, win_streak, win_count)
    and returns them as a dictionary of dictionaries.

    NOTE: This is dummy logic. Replace with actual DB query 
    if persistence is required.
    """
    print("Fetching scores (using dummy data)")
    # Return a copy of the entire player-stats dictionary
    return {player: stats.copy() for player, stats in _player_stats.items()}

# --- Call initialization automatically upon module import ---
initialize_database()
