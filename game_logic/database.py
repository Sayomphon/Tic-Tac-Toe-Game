# game_logic/database.py
import sqlite3
import os
from typing import Dict, Any

# --- Configuration ---
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'db', 'tic_tac_toe.db')

# --- Dummy Data (ปรับปรุงให้เก็บ win_count) ---
# ใช้ dictionary ที่ซับซ้อนขึ้นเพื่อจำลอง DB structure
# { player_name: {"score": int, "win_streak": int, "win_count": int} }
_player_stats: Dict[str, Dict[str, int]] = {
    "Player1": {"score": 0, "win_streak": 0, "win_count": 0},
    "Bot": {"score": 0, "win_streak": 0, "win_count": 0} # เพิ่ม Bot ด้วย
}

# --- Database Functions ---

def initialize_database():
    """Creates the database and table if they don't exist."""
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # เพิ่มคอลัมน์ win_count
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT UNIQUE NOT NULL,
                score INTEGER DEFAULT 0,
                win_streak INTEGER DEFAULT 0,
                win_count INTEGER DEFAULT 0  -- เพิ่มคอลัมน์นี้
            )
        ''')
        # Optional: เพิ่มผู้เล่นเริ่มต้นถ้ายังไม่มี
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
    """Helper to add player to dummy data if not exists."""
    global _player_stats
    if player_name not in _player_stats:
        _player_stats[player_name] = {"score": 0, "win_streak": 0, "win_count": 0}
        print(f"Initialized dummy stats for {player_name}")

def update_score(player_name: str, result: str):
    """
    Updates player score, win streak, and win count based on game result.
    'win', 'loss', 'tie'
    """
    # --- Placeholder Logic using dictionary ---
    global _player_stats
    _ensure_player_exists(player_name) # ตรวจสอบว่ามีผู้เล่นใน dummy data หรือยัง

    stats = _player_stats[player_name]

    if result == "win":
        stats["score"] += 1
        stats["win_count"] += 1 # เพิ่มจำนวนชนะ
        stats["win_streak"] += 1
        if stats["win_streak"] == 3:
            print(f"{player_name} got a 3-win streak bonus!")
            stats["score"] += 1 # Bonus point
            stats["win_streak"] = 0 # Reset streak
    elif result == "loss":
        stats["score"] -= 1
        stats["win_streak"] = 0 # Reset streak on loss
        # win_count ไม่เพิ่ม
    elif result == "tie":
        stats["win_streak"] = 0 # Reset streak on tie
        # win_count และ score ไม่เปลี่ยน

    print(f"Updated stats for {player_name}: Score={stats['score']}, Streak={stats['win_streak']}, Wins={stats['win_count']}")

    # --- TODO: Replace above with actual SQLite update ---
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # try:
    #     # ดึงข้อมูลปัจจุบัน
    #     cursor.execute("SELECT score, win_streak, win_count FROM scores WHERE player_name = ?", (player_name,))
    #     row = cursor.fetchone()
    #     if not row: # ถ้ายังไม่มีผู้เล่น ให้ INSERT ก่อน (ควรจะถูกสร้างใน initialize แล้ว)
    #         cursor.execute("INSERT INTO scores (player_name, score, win_streak, win_count) VALUES (?, 0, 0, 0)", (player_name,))
    #         current_score, current_streak, current_wins = 0, 0, 0
    #     else:
    #         current_score, current_streak, current_wins = row
    #
    #     # คำนวณค่าใหม่
    #     new_score = current_score
    #     new_streak = current_streak
    #     new_wins = current_wins
    #
    #     if result == "win":
    #         new_score += 1
    #         new_wins += 1
    #         new_streak += 1
    #         if new_streak == 3:
    #             new_score += 1 # Bonus
    #             new_streak = 0 # Reset
    #     elif result == "loss":
    #         new_score -= 1
    #         new_streak = 0
    #     elif result == "tie":
    #         new_streak = 0
    #
    #     # อัปเดตฐานข้อมูล
    #     cursor.execute("""
    #         UPDATE scores
    #         SET score = ?, win_streak = ?, win_count = ?
    #         WHERE player_name = ?
    #     """, (new_score, new_streak, new_wins, player_name))
    #     conn.commit()
    # except sqlite3.Error as e:
    #     print(f"Database error updating score for {player_name}: {e}")
    # finally:
    #     conn.close()


def reset_scores():
    """
    Resets all player scores, win streaks, and win counts to 0.
    """
    global _player_stats
    # Reset dummy data
    for player in _player_stats:
        _player_stats[player] = {"score": 0, "win_streak": 0, "win_count": 0}
    print("Dummy scores have been reset.")

    # --- TODO: Replace/Add actual SQLite update ---
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
    """Returns all player stats (score, win_streak, win_count)."""
    # --- Placeholder Logic using dictionary ---
    print("Fetching scores (using dummy data)")
    # คืนค่าสำเนาของ dictionary ทั้งหมด
    return {player: stats.copy() for player, stats in _player_stats.items()}

    # --- TODO: Replace above with actual SQLite select ---
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # player_stats_from_db = {}
    # try:
    #     cursor.execute("SELECT player_name, score, win_streak, win_count FROM scores")
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         player_name, score, win_streak, win_count = row
    #         player_stats_from_db[player_name] = {
    #             "score": score,
    #             "win_streak": win_streak,
    #             "win_count": win_count
    #         }
    # except sqlite3.Error as e:
    #     print(f"Database error fetching scores: {e}")
    # finally:
    #     conn.close()
    # return player_stats_from_db

# --- Call initialization when the module is loaded ---
initialize_database()