// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Element References ---
    const bodyElement = document.body; // <--- เพิ่ม: อ้างอิงถึง body สำหรับเปลี่ยน Theme
    const gameContainer = document.querySelector('.game-container');
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const restartButton = document.getElementById('restart-button');
    // Score elements
    const playerScoreElement = document.getElementById('player-score');
    const botScoreElement = document.getElementById('bot-score');
    // Win count elements
    const playerWinsElement = document.getElementById('player-wins');
    const botWinsElement = document.getElementById('bot-wins');
    // Difficulty elements
    const difficultySegments = document.querySelectorAll('.segmented-control .segment'); // Selector for segmented control buttons
    const difficultyDescription = document.getElementById('difficulty-description'); // Description element

    // Descriptions for each level (optional but recommended)
    const difficultyDescriptions = {
        easy: "Easy: AI plays randomly.",
        medium: "Medium: AI sometimes plays randomly.",
        hard: "Hard: AI uses Minimax strategy."
    };

    // --- Game State Variables ---
    let currentBoard = ["", "", "", "", "", "", "", "", ""]; // Represents the 3x3 board
    let gameActive = true; // Tracks if the game is currently playable
    const playerMark = 'X';
    const botMark = 'O';
    let currentDifficulty = 'easy'; // Default difficulty, will be updated by initializeDifficulty
    const resetDelay = 3000; // Delay in milliseconds before resetting the board after a game ends (ใช้ค่าเดิมที่คุณให้มา)

    // --- Initialize Difficulty Based on UI ---
    function initializeDifficulty() {
        let foundActive = false;
        difficultySegments.forEach(segment => {
            if (segment.classList.contains('active')) {
                currentDifficulty = segment.dataset.difficulty;
                foundActive = true;
                if (difficultyDescription && difficultyDescriptions[currentDifficulty]) {
                    difficultyDescription.textContent = difficultyDescriptions[currentDifficulty];
                }
                // **** เพิ่ม: ตั้งค่า theme class เริ่มต้น ****
                updateThemeClass(currentDifficulty);
            }
        });
        if (!foundActive) {
             const easyButton = document.querySelector('.segmented-control .segment[data-difficulty="easy"]');
             if (easyButton) {
                easyButton.classList.add('active');
                currentDifficulty = 'easy';
                 if (difficultyDescription && difficultyDescriptions[currentDifficulty]) {
                    difficultyDescription.textContent = difficultyDescriptions[currentDifficulty];
                 }
                 // **** เพิ่ม: ตั้งค่า theme class เริ่มต้น ****
                 updateThemeClass(currentDifficulty);
             }
        }
         console.log("Initial difficulty set to:", currentDifficulty);
    }

    // --- **** เพิ่ม: ฟังก์ชันอัปเดต Theme Class **** ---
    function updateThemeClass(difficulty) {
        if (!gameContainer) return; // ป้องกัน error ถ้าหา gameContainer ไม่เจอ

        // ลบคลาส theme เก่าทั้งหมดออกจาก gameContainer (ไม่ใช่ body)
        gameContainer.classList.remove('difficulty-easy', 'difficulty-medium', 'difficulty-hard');
    
        // เพิ่มคลาส theme ใหม่ตาม difficulty ที่เลือก ให้กับ gameContainer
        if (difficulty) {
             gameContainer.classList.add(`difficulty-${difficulty}`);
        } else {
             gameContainer.classList.add('difficulty-easy'); // Fallback
        }
        console.log("Applied theme class to game-container:", `difficulty-${difficulty || 'easy'}`);
    }


    // --- Event Listener for Difficulty Selection ---
    difficultySegments.forEach(segment => {
        segment.addEventListener('click', (event) => {
            const clickedButton = event.currentTarget;
            const selectedDifficulty = clickedButton.dataset.difficulty;

            if (currentDifficulty !== selectedDifficulty) {
                 currentDifficulty = selectedDifficulty;
                 console.log("Difficulty changed to:", currentDifficulty);

                 difficultySegments.forEach(btn => btn.classList.remove('active'));
                 clickedButton.classList.add('active');

                 if (difficultyDescription && difficultyDescriptions[selectedDifficulty]) {
                     difficultyDescription.textContent = difficultyDescriptions[selectedDifficulty];
                 }

                 // **** เพิ่ม: เรียกใช้ฟังก์ชันอัปเดต Theme ****
                 updateThemeClass(selectedDifficulty);
            }
        });
    });


    // --- Initialization and Board Setup ---
    function createBoard() {
        boardElement.innerHTML = ''; // Clear previous board cells if any
        currentBoard.forEach((_, index) => {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = index;
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        });
        updateBoardDisplay(); // Ensure the visual board matches the initial empty state
    }

    // --- UI Updates ---
    function updateBoardDisplay() {
        const cells = boardElement.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            cell.textContent = currentBoard[index];
            cell.classList.remove(playerMark, botMark);
            if (currentBoard[index]) {
                cell.classList.add(currentBoard[index]);
            }
        });
    }

    function updateStatus(message) {
        statusElement.textContent = message;
    }

    // --- Game Logic and Handling Moves ---
    async function handleCellClick(event) {
        if (!gameActive) return;

        const index = parseInt(event.target.dataset.index);

        if (currentBoard[index] !== "" || !gameActive) return;

        // --- Player's Move ---
        currentBoard[index] = playerMark;
        updateBoardDisplay();

        // --- Check for Player Win or Tie ---
        if (checkLocalWin(playerMark)) {
            await handleGameOver("Player1", "win"); // เรียก handleGameOver แล้วจบเลย
            // ไม่ต้องมี setTimeout(resetBoard, resetDelay); ซ้ำตรงนี้
            return;
        }
        if (isBoardFull()) {
             await handleGameOver("Player1", "tie"); // เรียก handleGameOver แล้วจบเลย
             // ไม่ต้องมี setTimeout(resetBoard, resetDelay); ซ้ำตรงนี้
            return;
        }

        // --- AI's Turn ---
        updateStatus(`AI (${currentDifficulty}) is thinking...`);
        gameActive = false;

        await new Promise(resolve => setTimeout(resolve, 250)); // Optional delay

        try {
            const response = await fetch('/api/play', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    board: currentBoard,
                    difficulty: currentDifficulty
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Server error occurred.' }));
                throw new Error(errorData.detail || 'Network response was not ok');
            }

            const data = await response.json();
            currentBoard = data.new_board;
            updateBoardDisplay();
            updateStatus(data.message);

            // --- Check for AI Win or Tie after AI's move ---
            if (data.winner === botMark) {
                await handleGameOver("Player1", "loss"); // เรียก handleGameOver
                // ไม่ต้องมี setTimeout(resetBoard, resetDelay); ซ้ำตรงนี้
            } else if (data.is_tie) {
                await handleGameOver("Player1", "tie"); // เรียก handleGameOver
                // ไม่ต้องมี setTimeout(resetBoard, resetDelay); ซ้ำตรงนี้
            } else {
                gameActive = true; // Game continues
            }
        } catch (error) {
            console.error("Error during AI turn:", error);
            updateStatus(`Error: ${error.message}. Please try restarting the game.`);
            gameActive = false;
        }
    }

    // --- Helper Functions ---
    function checkLocalWin(mark) {
        const winConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6]             // Diagonals
        ];
        return winConditions.some(condition =>
            condition.every(index => currentBoard[index] === mark)
        );
    }

    function isBoardFull() {
        return currentBoard.every(cell => cell !== "");
    }

    function resetBoard() {
        currentBoard = ["", "", "", "", "", "", "", "", ""];
        gameActive = true;
        updateBoardDisplay();
    }

    // --- Score Management ---
    async function updateScoreAPI(playerName, result) {
        try {
            const response = await fetch('/api/update_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_name: playerName, result: result }),
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
        try {
            const response = await fetch('/api/get_scores');
            if (!response.ok) throw new Error(`Failed to fetch scores. Status: ${response.status}`);
            const data = await response.json();

            const playerStats = data.scores["Player1"] || { score: 0, win_count: 0, win_streak: 0 };
            const botStats = data.scores["Bot"] || { score: 0, win_count: 0, win_streak: 0 };

            playerScoreElement.textContent = playerStats.score;
            botScoreElement.textContent = botStats.score;
            playerWinsElement.textContent = playerStats.win_count;
            botWinsElement.textContent = botStats.win_count;

        } catch (error) {
            console.error("Error fetching scores:", error);
            playerScoreElement.textContent = '-';
            botScoreElement.textContent = '-';
            playerWinsElement.textContent = '-';
            botWinsElement.textContent = '-';
        }
    }

    // --- Game Over Handling ---
    async function handleGameOver(playerName, playerResult) {
        gameActive = false;
        console.log(`Game Over. Player: ${playerName}, Result: ${playerResult}`);

        let finalStatus = "";
        if (playerResult === "win") {
            finalStatus = "You win!";
        } else if (playerResult === "loss") {
            finalStatus = "AI wins!";
        } else {
            finalStatus = "It's a Tie!";
        }
        updateStatus(finalStatus);

        // Update scores for both players
        await updateScoreAPI(playerName, playerResult);
        if (playerResult === "loss") {
            await updateScoreAPI("Bot", "win");
        } else if (playerResult === "win") {
            await updateScoreAPI("Bot", "loss");
        } else if (playerResult === "tie") {
            await updateScoreAPI("Bot", "tie");
        }

        await fetchScores(); // Fetch scores after updates are sent

        // --- นี่คือส่วนที่จัดการการ Delay และ Reset Board ---
        setTimeout(() => {
             console.log("Timeout finished, preparing for new game.");
             resetBoard(); // Reset board state and make game active again
             updateStatus("New Game! Your turn (X)"); // Set status for the new round
        }, resetDelay); // ใช้ค่า resetDelay ที่กำหนดไว้ (3000ms)
    }


    // --- Restart Game Completely ---
    async function restartGame() {
        console.log("Restarting game and resetting scores...");
        gameActive = false;
        try {
            await fetch('/api/reset_scores', { method: 'POST' });
            console.log("Server scores reset request sent.");

            await fetchScores();
            console.log("Fetched reset scores.");

            resetBoard();

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
            // **** เพิ่ม: Reset Theme Class ****
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

    // --- Event Listeners ---
    restartButton.addEventListener('click', restartGame);

    // --- Initial Game Setup When Page Loads ---
    initializeDifficulty(); // Set difficulty and initial theme based on UI state
    createBoard();        // Create the initial empty board UI
    fetchScores();        // Fetch and display scores from the backend
    updateStatus("Your turn (X)"); // Set the initial prompt for the player
});