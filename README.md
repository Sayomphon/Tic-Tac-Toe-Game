# Tic-Tac-Toe AI Game

A web-based Tic-Tac-Toe game where you play against an AI opponent with varying difficulty levels. Built with Python, FastAPI, and vanilla JavaScript, featuring a scoring system with win streak bonuses.

## ✨ Features

* Classic Tic-Tac-Toe gameplay (Player 'X' vs. AI Bot 'O').
* AI opponent with adjustable difficulty levels (Easy, Medium, Hard) powered by the Minimax algorithm.
* Score tracking system: +1 point for a win, -1 point for a loss.
* Win streak bonus: Earn an extra +1 point after 3 consecutive wins (streak then resets).
* View current scores and total wins for both the player and the bot.
* Responsive web interface.
* Difficulty-based UI themes.
* Ability to reset all scores and start fresh.

## 📸 Demo / Screenshot

![image](https://github.com/Sayomphon/Tic-Tac-Toe-Game/blob/main/Pictures/playing%20hard.png)


## 💻 Technologies Used

* **Backend:** Python 3.7+, FastAPI
* **AI Logic:** Minimax Algorithm
* **Database:** SQLite (for score persistence)
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Server:** Uvicorn ASGI Server

## 🚀 Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Prerequisites:**
    * **Python:** Ensure you have Python 3.7 or newer installed. You can download it from [python.org](https://www.python.org/). Verify installation by running `python --version` or `python3 --version` in your terminal.
    * **pip:** Python's package installer, usually comes with Python. Verify with `pip --version`.
    * **Git:** Needed to clone the repository. Download from [git-scm.com](https://git-scm.com/).
    * **Code Editor:** A text editor like VS Code ([code.visualstudio.com](https://code.visualstudio.com/)) is recommended for viewing and editing code.

2.  **Clone the Repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/Sayomphon/Tic-Tac-Toe-Game.git
    
    cd Tic-Tac-Toe-Game
    ```

3.  **Create and Activate a Virtual Environment (Recommended):**
    This isolates project dependencies.
    ```bash
    # Create the virtual environment folder (e.g., named 'venv')
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    
    # On macOS/Linux:
    source venv/bin/activate
    ```
    You should see `(venv)` at the beginning of your terminal prompt.

4.  **Install Dependencies:**
    Install the required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure `requirements.txt` includes at least `fastapi` and `uvicorn[standard]`)*

## ▶️ Running the Application

1.  Make sure you are in the project's root directory (`Tic-Tac-Toe-Game`) and your virtual environment (`venv`) is activated.
2.  Run the FastAPI development server using Uvicorn:
    ```bash
    uvicorn app:app --reload
    ```
    * `app:app` refers to the `app` instance inside the `app.py` file.
    * `--reload` automatically restarts the server when you save code changes (convenient for development).
3.  The terminal will show output indicating the server is running, usually on `http://127.0.0.1:8000`.
4.  Open your web browser and navigate to `http://127.0.0.1:8000`.

## 🎮 How to Play

1.  **Load the Game:** Access the URL provided by Uvicorn (`http://127.0.0.1:8000`).
2.  **Select AI Difficulty:** Before starting or during the game, click the "Easy", "Medium", or "Hard" buttons under "AI Level". The interface colors will change to reflect the chosen difficulty.
3.  **Make Your Move:** You play as 'X'. Click on any empty square on the 3x3 grid.
4.  **AI Responds:** The computer (Bot 'O') will automatically make its move. Its strategy depends on the selected difficulty.
5.  **Game Progress:** Continue taking turns until a player gets three marks in a row (horizontally, vertically, or diagonally) or until all squares are filled (a tie).
6.  **Game End & Scoring:**
    * The status message will announce the winner or if it's a tie.
    * Scores are updated automatically (+1 for a win, -1 for a loss, 0 for a tie).
    * If you win 3 times consecutively, you get an extra bonus point, and the streak resets.
    * The displayed scores and win counts will update.
    * The board will automatically clear after a 3-second delay, ready for the next round.
7.  **Reset Scores:** If you want to reset all scores (Player and Bot) and win streaks back to zero, click the "Reset Scores & New Game" button.

## ⚙️ Technical Details & Concepts

This project implements the specific requirements using the following techniques:

* **Player vs. AI Bot:** The core gameplay loop manages turns between the human player ('X') interacting via the web interface and the computer-controlled opponent ('O') whose moves are determined by the backend AI logic.
* **AI Implementation (Minimax):**
    * The bot's intelligence is primarily driven by the **Minimax algorithm**. This algorithm explores possible future game states to choose the move that leads to the best outcome for the AI, assuming the player also plays optimally. It's well-suited for deterministic, perfect-information games like Tic-Tac-Toe.
    * **Difficulty Levels:**
        * **Easy:** The AI selects a random available square, offering no strategic challenge.
        * **Medium:** The AI mixes strategies. It has a chance (currently 50% in the code) to play randomly, otherwise it uses the Minimax algorithm. This adds unpredictability.
        * **Hard:** The AI consistently uses the Minimax algorithm to select the optimal move available, making it very difficult (or impossible) to beat.
* **Scoring System:**
    * A persistent score is maintained using an **SQLite database** (`db/tic_tac_toe.db`), managed by `game_logic/database.py`. The database stores `player_name`, `score`, `win_streak`, and `win_count`.
    * **Win/Loss Points:** When a game ends, the backend receives the result (`win`, `loss`, or `tie`) via the `/api/update_score` endpoint. It adjusts the score accordingly (+1 for win, -1 for loss).
    * **Win Streak Bonus:** The `database.py` logic increments a `win_streak` counter on each win. If the streak reaches 3, an additional +1 bonus point is added to the `score`, and the `win_streak` is reset to 0. The streak also resets to 0 on a loss or tie.
* **Score Viewing:** The frontend uses JavaScript's `Workspace` to call the `/api/get_scores` endpoint. This endpoint retrieves the current statistics (score, win streak, total wins) for all known players ("Player1", "Bot") from the database and returns them as JSON. The JavaScript then updates the corresponding HTML elements on the page.
* **Web Framework (FastAPI):** FastAPI handles incoming HTTP requests, routes them to the appropriate Python functions (defined in `routers/game_router.py`), validates request data (using Pydantic models), calls the game/database logic, and returns JSON responses to the frontend. It also serves the static files (HTML, CSS, JS).

## 📂 Project Structure
![image](https://github.com/Sayomphon/Tic-Tac-Toe-Game/blob/main/Pictures/Project%20structure.png)