// static/script.js
// ------------------------------------------------------------
//  Client‑side logic for the Tic‑Tac‑Toe (OX) web application.
//  ▸ Renders the board and listens for user interactions.
//  ▸ Sends/receives data to/from the FastAPI backend.
//  ▸ Manages difficulty selection, theming, score updates, and
//    game‑over flow.
//
//  IMPORTANT:  Only comments were added; no code was altered.
// ------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    // --------------------------------------------------------
    //  Element References
    // --------------------------------------------------------
    const bodyElement      = document.body;                         // <--- reference to <body> (kept for potential global theming)
    const gameContainer    = document.querySelector('.game-container');
    const boardElement     = document.getElementById('board');
    const statusElement    = document.getElementById('status');
    const restartButton    = document.getElementById('restart-button');

    //  Score display elements
    const playerScoreElement = document.getElementById('player-score');
    const botScoreElement    = document.getElementById('bot-score');

    //  Win‑count display elements
    const playerWinsElement  = document.getElementById('player-wins');
    const botWinsElement     = document.getElementById('bot-wins');

    //  Difficulty‑selector elements
    const difficultySegments   = document.querySelectorAll('.segmented-control .segment');
    const difficultyDescription = document.getElementById('difficulty-description');

    //  Human‑readable descriptions for each AI level (used in UI)
    const difficultyDescriptions = {
        easy   : "Easy: AI plays randomly.",
        medium : "Medium: AI sometimes plays randomly.",
        hard   : "Hard: AI uses Minimax strategy."
    };

    // --------------------------------------------------------
    //  Game‑state variables (kept in memory on the client)
    // --------------------------------------------------------
    let currentBoard   = ["", "", "", "", "", "", "", "", ""]; // flat 3×3 board
    let gameActive     = true;                                 // true = player can click
    const playerMark   = 'X';
    const botMark      = 'O';
    let currentDifficulty = 'easy';                            // default; updated by initializeDifficulty()
    const resetDelay   = 3000;                                 // ms to wait before starting next round

    // --------------------------------------------------------
    //  Initialise difficulty from UI (called on page load)
    // --------------------------------------------------------
    function initializeDifficulty() {
        let foundActive = false;

        difficultySegments.forEach(segment => {
            if (segment.classList.contains('active')) {
                // a segment is already marked as active in the HTML
                currentDifficulty = segment.dataset.difficulty;
                foundActive = true;

                // update helper text
                if (difficultyDescription && difficultyDescriptions[currentDifficulty]) {
                    difficultyDescription.textContent = difficultyDescriptions[currentDifficulty];
                }
                // apply CSS theme
                updateThemeClass(currentDifficulty);
            }
        });

        // if nothing was active, default to EASY
        if (!foundActive) {
            const easyButton = document.querySelector('.segmented-control .segment[data-difficulty="easy"]');
            if (easyButton) {
                easyButton.classList.add('active');
                currentDifficulty = 'easy';

                if (difficultyDescription && difficultyDescriptions[currentDifficulty]) {
                    difficultyDescription.textContent = difficultyDescriptions[currentDifficulty];
                }
                updateThemeClass(currentDifficulty);
            }
        }
        console.log("Initial difficulty set to:", currentDifficulty);
    }

    // --------------------------------------------------------
    //  Apply difficulty‑specific CSS class for easy styling
    // --------------------------------------------------------
    function updateThemeClass(difficulty) {
        if (!gameContainer) return; // safety check

        // remove any previous difficulty class
        gameContainer.classList.remove('difficulty-easy', 'difficulty-medium', 'difficulty-hard');

        // add new difficulty class (or fallback to easy)
        if (difficulty) {
            gameContainer.classList.add(`difficulty-${difficulty}`);
        } else {
            gameContainer.classList.add('difficulty-easy');
        }
        console.log("Applied theme class to game-container:", `difficulty-${difficulty || 'easy'}`);
    }

    // --------------------------------------------------------
    //  Difficulty button click handler
    // --------------------------------------------------------
    difficultySegments.forEach(segment => {
        segment.addEventListener('click', (event) => {
            const clickedButton      = event.currentTarget;
            const selectedDifficulty = clickedButton.dataset.difficulty;

            if (currentDifficulty !== selectedDifficulty) {
                currentDifficulty = selectedDifficulty;
                console.log("Difficulty changed to:", currentDifficulty);

                // visual toggle
                difficultySegments.forEach(btn => btn.classList.remove('active'));
                clickedButton.classList.add('active');

                // update helper text
                if (difficultyDescription && difficultyDescriptions[selectedDifficulty]) {
                    difficultyDescription.textContent = difficultyDescriptions[selectedDifficulty];
                }

                // update CSS theme
                updateThemeClass(selectedDifficulty);
            }
        });
    });

    // --------------------------------------------------------
    //  Board creation (called once on load or after reset)
    // --------------------------------------------------------
    function createBoard() {
        boardElement.innerHTML = ''; // clear previous cells
        currentBoard.forEach((_, index) => {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = index.toString();
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        });
        updateBoardDisplay(); // sync UI with initial empty board
    }

    // --------------------------------------------------------
    //  Render the board array to the DOM
    // --------------------------------------------------------
    function updateBoardDisplay() {
        const cells = boardElement.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            cell.textContent = currentBoard[index];           // show 'X' or 'O'
            cell.classList.remove(playerMark, botMark);       // reset CSS classes
            if (currentBoard[index]) {
                cell.classList.add(currentBoard[index]);      // add class 'X' or 'O' for styling
            }
        });
    }

    // helper to update the status text
    function updateStatus(message) {
        statusElement.textContent = message;
    }

    // --------------------------------------------------------
    //  Main click handler for a board cell (player's turn)
    // --------------------------------------------------------
    async function handleCellClick(event) {
        if (!gameActive) return;

        const index = parseInt(event.target.dataset.index, 10);

        // ignore click if cell is occupied
        if (currentBoard[index] !== "" || !gameActive) return;

        // ----- Player's move -----
        currentBoard[index] = playerMark;
        updateBoardDisplay();

        // check win / tie after player's move
        if (checkLocalWin(playerMark)) {
            await handleGameOver("Player1", "win");
            return; // stop further processing
        }
        if (isBoardFull()) {
            await handleGameOver("Player1", "tie");
            return;
        }

        // ----- AI's turn -----
        updateStatus(`AI (${currentDifficulty}) is thinking...`);
        gameActive = false; // lock UI while waiting for server

        // optional small delay for realism
        await new Promise(resolve => setTimeout(resolve, 250));

        try {
            // send current board + difficulty to backend
            const response = await fetch('/api/play', {
                method : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body   : JSON.stringify({
                    board     : currentBoard,
                    difficulty: currentDifficulty
                }),
            });

            if (!response.ok) {
                // attempt to parse JSON error; fallback generic
                const errorData = await response.json().catch(() => ({ detail: 'Server error occurred.' }));
                throw new Error(errorData.detail || 'Network response was not ok');
            }

            // parse backend response
            const data = await response.json();
            currentBoard = data.new_board;
            updateBoardDisplay();
            updateStatus(data.message);

            // evaluate result of AI move
            if (data.winner === botMark) {
                await handleGameOver("Player1", "loss");
            } else if (data.is_tie) {
                await handleGameOver("Player1", "tie");
            } else {
                gameActive = true; // continue game
            }
        } catch (error) {
            console.error("Error during AI turn:", error);
            updateStatus(`Error: ${error.message}. Please try restarting the game.`);
            gameActive = false;
        }
    }

    // --------------------------------------------------------
    //  Utility helpers (pure JS, no server calls)
    // --------------------------------------------------------
    function checkLocalWin(mark) {
        const winConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
            [0, 4, 8], [2, 4, 6]             // diagonals
        ];
        return winConditions.some(condition =>
            condition.every(index => currentBoard[index] === mark)
        );
    }

    function isBoardFull() {
        return currentBoard.every(cell => cell !== "");
    }

    // reset board (does NOT touch scores)
    function resetBoard() {
        currentBoard = ["", "", "", "", "", "", "", "", ""];
        gameActive   = true;
        updateBoardDisplay();
    }

    // --------------------------------------------------------
    //  Score management helpers (REST calls)
    // --------------------------------------------------------
    async function updateScoreAPI(playerName, result) {
        // sends POST /api/update_score
        try {
            const response = await fetch('/api/update_score', {
                method : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body   : JSON.stringify({ player_name: playerName, result: result }),
            });
            if (!response.ok) {
                console.error(`Failed to update score for ${playerName}. Status: ${response.status}`);
            } else {
                console.log(`Score update request sent for ${playerName} with result: ${result}`);
            }
        } catch (error) {
            console.error(`Error updating score for ${playerName}:`, error);
        }
    }

    async function fetchScores() {
        // GET /api/get_scores → update score UI
        try {
            const response = await fetch('/api/get_scores');
            if (!response.ok) throw new Error(`Failed to fetch scores. Status: ${response.status}`);

            const data = await response.json();

            // fallbacks in case backend returns nothing
            const playerStats = data.scores["Player1"] || { score: 0, win_count: 0, win_streak: 0 };
            const botStats    = data.scores["Bot"]    || { score: 0, win_count: 0, win_streak: 0 };

            // update DOM
            playerScoreElement.textContent = playerStats.score;
            botScoreElement.textContent    = botStats.score;
            playerWinsElement.textContent  = playerStats.win_count;
            botWinsElement.textContent     = botStats.win_count;

        } catch (error) {
            console.error("Error fetching scores:", error);
            playerScoreElement.textContent = '-';
            botScoreElement.textContent    = '-';
            playerWinsElement.textContent  = '-';
            botWinsElement.textContent     = '-';
        }
    }

    // --------------------------------------------------------
    //  Handle end‑of‑game logic (update scores + UI + restart)
    // --------------------------------------------------------
    async function handleGameOver(playerName, playerResult) {
        gameActive = false;
        console.log(`Game Over. Player: ${playerName}, Result: ${playerResult}`);

        // set status banner
        let finalStatus = "";
        if (playerResult === "win")      finalStatus = "You win!";
        else if (playerResult === "loss")finalStatus = "AI wins!";
        else                              finalStatus = "It's a Tie!";
        updateStatus(finalStatus);

        // update server‑side scores (player & bot)
        await updateScoreAPI(playerName, playerResult);
        if (playerResult === "loss") {
            await updateScoreAPI("Bot", "win");
        } else if (playerResult === "win") {
            await updateScoreAPI("Bot", "loss");
        } else {
            await updateScoreAPI("Bot", "tie");
        }

        await fetchScores(); // refresh scoreboard

        // wait a bit, then start a new round
        setTimeout(() => {
            console.log("Timeout finished, preparing for new game.");
            resetBoard();
            updateStatus("New Game! Your turn (X)");
        }, resetDelay);
    }

    // --------------------------------------------------------
    //  Full game restart (scores + board + difficulty reset)
    // --------------------------------------------------------
    async function restartGame() {
        console.log("Restarting game and resetting scores...");
        gameActive = false;

        try {
            // tell backend to zero out all scores
            await fetch('/api/reset_scores', { method: 'POST' });
            console.log("Server scores reset request sent.");

            // update local scoreboard
            await fetchScores();
            console.log("Fetched reset scores.");

            // clear board
            resetBoard();

            // reset difficulty UI to EASY
            const defaultDifficulty = 'easy';
            difficultySegments.forEach(segment => {
                if (segment.dataset.difficulty === defaultDifficulty) {
                    segment.classList.add('active');
                } else {
                    segment.classList.remove('active');
                }
            });
            currentDifficulty = defaultDifficulty;

            if (difficultyDescription && difficultyDescriptions[currentDifficulty]) {
                difficultyDescription.textContent = difficultyDescriptions[currentDifficulty];
            }
            updateThemeClass(defaultDifficulty);
            console.log("Difficulty reset to:", currentDifficulty);

            gameActive = true;
            updateStatus("Scores Reset! Your turn (X)");
            console.log("Game ready.");

        } catch (error) {
            console.error("Error during full game restart:", error);
            updateStatus("Error restarting game. Please refresh.");
        }
    }

    // --------------------------------------------------------
    //  Attach event listeners
    // --------------------------------------------------------
    restartButton.addEventListener('click', restartGame);

    // --------------------------------------------------------
    //  Initial setup on first page load
    // --------------------------------------------------------
    initializeDifficulty();  // set difficulty + theme
    createBoard();           // render empty board
    fetchScores();           // pull scores from backend
    updateStatus("Your turn (X)");
});
