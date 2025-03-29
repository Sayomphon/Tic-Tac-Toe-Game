# game_logic/database.py
import sqlite3
import os

# --- Configuration ---
# Get the absolute path of the current script file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the database file relative to the current script
db_path = os.path.join(current_dir, '..', 'db', 'tic_tac_toe.db') # Navigate up one level then into db/

# --- Dummy Data (Replace with actual DB interaction later) ---
# Using a simple dictionary for now to simulate scores
# In a real app, this would interact with the SQLite DB
_scores = {"Player1": 5, "Bot": -2}
_win_streaks = {"Player1": 1}

# --- Database Functions (Placeholders/Basic Structure) ---

def initialize_database():
    """Creates the database and table if they don't exist."""
    try:
        # Ensure the db directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Example table - adjust columns as needed
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT UNIQUE NOT NULL,
                score INTEGER DEFAULT 0,
                win_streak INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Database initialized/checked at: {db_path}")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during DB initialization: {e}")


def update_score(player_name: str, result: str):
    """
    Updates player score and win streak based on game result.
    'win', 'loss', 'tie'
    """
    # --- Placeholder Logic using dictionary ---
    global _scores, _win_streaks
    if player_name not in _scores:
        _scores[player_name] = 0
        _win_streaks[player_name] = 0

    if result == "win":
        _scores[player_name] += 1
        _win_streaks[player_name] += 1
        if _win_streaks[player_name] == 3:
            print(f"{player_name} got a 3-win streak bonus!")
            _scores[player_name] += 1 # Bonus point
            _win_streaks[player_name] = 0 # Reset streak
    elif result == "loss":
        _scores[player_name] -= 1
        _win_streaks[player_name] = 0 # Reset streak on loss
    elif result == "tie":
        _win_streaks[player_name] = 0 # Reset streak on tie

    print(f"Updated score for {player_name}: {_scores[player_name]}, Streak: {_win_streaks[player_name]}")
    # --- TODO: Replace above with actual SQLite update ---
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # ... logic to fetch current score/streak, update, and commit ...
    # conn.close()

def get_scores() -> dict:
    """Returns all player scores."""
    # --- Placeholder Logic using dictionary ---
    print("Fetching scores (using dummy data)")
    return _scores.copy() # Return a copy to prevent external modification
    # --- TODO: Replace above with actual SQLite select ---
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC")
    # scores_data = dict(cursor.fetchall())
    # conn.close()
    # return scores_data

# --- Call initialization when the module is loaded ---
# Be careful with running initialization directly on import in complex apps,
# but for this simple case it's okay.
initialize_database()