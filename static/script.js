// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const restartButton = document.getElementById('restart-button');
    const scoresElement = document.getElementById('scores-list'); // Ensure you have an element with id="scores-list"

    let currentBoard = ["", "", "", "", "", "", "", "", ""];
    let gameActive = true;
    const playerMark = 'X';
    const aiMark = 'O';

    // --- Initialize Board ---
    function createBoard() {
        boardElement.innerHTML = ''; // Clear previous board
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = i; // Store index in data attribute
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        }
        updateBoardDisplay(); // Ensure initial empty board is shown
    }

    // --- Update UI ---
    function updateBoardDisplay() {
        const cells = boardElement.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            cell.textContent = currentBoard[index];
            cell.classList.remove('X', 'O'); // Clear previous marks
            if (currentBoard[index] === 'X') {
                cell.classList.add('X');
            } else if (currentBoard[index] === 'O') {
                cell.classList.add('O');
            }
        });
    }

    function updateStatus(message) {
        statusElement.textContent = message;
    }

    // --- Handle Player Move ---
    async function handleCellClick(event) {
        if (!gameActive) return;

        const clickedCell = event.target;
        const index = parseInt(clickedCell.dataset.index);

        if (currentBoard[index] !== "") {
            updateStatus("Cell already taken!");
            return;
        }

        // Player makes move
        currentBoard[index] = playerMark;
        updateBoardDisplay();

        // Check player win before sending to AI
        if (checkLocalWin(playerMark)) {
             updateStatus("You win!");
             gameActive = false;
             await updateScore("Player1", "win"); // Update score on win
             fetchScores(); // Refresh scores display
             return;
         }
         if (isBoardFull()) {
              updateStatus("It's a Tie!");
              gameActive = false;
              await updateScore("Player1", "tie"); // Update score on tie
              fetchScores(); // Refresh scores display
              return;
          }


        // Send board to backend for AI move
        updateStatus("AI is thinking...");
        try {
            const response = await fetch('/api/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ board: currentBoard }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Network response was not ok');
            }

            const data = await response.json();
            console.log("Received from backend:", data);

            currentBoard = data.new_board;
            updateBoardDisplay();
            updateStatus(data.message);

            if (data.winner) {
                gameActive = false;
                // Determine result from Player's perspective
                let result = "tie"; // Default to tie
                if (data.winner === playerMark) {
                   result = "win"; // Should have been caught earlier, but handle defensively
                } else if (data.winner === aiMark) {
                    result = "loss";
                }
                await updateScore("Player1", result); // Update score after AI potentially wins/ties
                fetchScores(); // Refresh scores display

            } else {
                 gameActive = true; // Game continues
            }


        } catch (error) {
            console.error('Error during API call:', error);
            updateStatus(`Error: ${error.message}`);
            gameActive = true; // Allow player to potentially retry? Or handle differently.
        }
    }

    // --- Helper functions for Win/Tie Check (Client-side for immediate feedback) ---
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


    // --- Handle Score Update ---
    async function updateScore(playerName, result) {
        try {
             console.log(`Updating score for ${playerName}, result: ${result}`);
             const response = await fetch('/api/update_score', {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify({ player_name: playerName, result: result }),
             });
             if (!response.ok) {
                 const errorData = await response.json();
                 throw new Error(errorData.detail || 'Failed to update score');
             }
             const data = await response.json();
             console.log("Score update response:", data.message);
         } catch (error) {
             console.error("Error updating score:", error);
             // Optionally display an error to the user
         }
    }

     // --- Fetch and Display Scores ---
     async function fetchScores() {
        const playerScoreElement = document.getElementById('player-score'); // Get new element
        const botScoreElement = document.getElementById('bot-score');     // Get new element
    
        try {
            const response = await fetch('/api/get_scores');
            if (!response.ok) {
                throw new Error('Failed to fetch scores');
            }
            const data = await response.json();
    
            playerScoreElement.textContent = '0';
            botScoreElement.textContent = '0';
    
            // Update with fetched scores
            if (data.scores["Player1"] !== undefined) { // Check if Player1 exists
                 playerScoreElement.textContent = data.scores["Player1"];
            }
             if (data.scores["Bot"] !== undefined) { // Check if Bot exists
                 botScoreElement.textContent = data.scores["Bot"];
             }
    
        } catch (error) {
            console.error("Error fetching scores:", error);
            if (playerScoreElement) playerScoreElement.textContent = '-'; // Show error indicator
            if (botScoreElement) botScoreElement.textContent = '-';
        }
    }
    
    // --- Restart Game ---
    function restartGame() {
        currentBoard = ["", "", "", "", "", "", "", "", ""];
        gameActive = true;
        updateStatus("Your turn (X)");
        createBoard(); // Recreate the board elements
        fetchScores(); // Update scores display on restart
    }

    // --- Event Listeners ---
    restartButton.addEventListener('click', restartGame);

    // --- Initial Setup ---
    restartGame(); // Start the game for the first time
});