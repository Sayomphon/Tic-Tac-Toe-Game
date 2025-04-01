// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const restartButton = document.getElementById('restart-button');
    // Score elements
    const playerScoreElement = document.getElementById('player-score');
    const botScoreElement = document.getElementById('bot-score');
    // Win count elements (เพิ่มเข้ามาใหม่)
    const playerWinsElement = document.getElementById('player-wins');
    const botWinsElement = document.getElementById('bot-wins');
    // Streak elements (ถ้าต้องการแสดง)
    // const playerStreakElement = document.getElementById('player-streak');
    // const botStreakElement = document.getElementById('bot-streak');


    let currentBoard = ["", "", "", "", "", "", "", "", ""];
    let gameActive = true;
    const playerMark = 'X';
    const botMark = 'O'; // กำหนด Bot Mark ไว้ด้วย

    // --- Initialization and Board Setup ---
    function createBoard() {
        boardElement.innerHTML = '';
        currentBoard.forEach((_, index) => { // ใช้ forEach แทน for loop ได้
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = index;
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        });
        updateBoardDisplay(); // อัปเดตครั้งแรก
    }

    // --- UI Updates ---
    function updateBoardDisplay() {
        const cells = boardElement.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            cell.textContent = currentBoard[index];
            cell.classList.remove(playerMark, botMark); // ลบทั้ง X และ O ออกก่อน
            if (currentBoard[index]) {
                cell.classList.add(currentBoard[index]); // แล้วค่อยเพิ่ม class ตาม mark
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
        if (currentBoard[index] !== "" || !gameActive) return; // ตรวจสอบซ้ำ

        // Player's Move
        currentBoard[index] = playerMark;
        updateBoardDisplay();

        // Check Player Win or Tie locally (Optional but good for immediate feedback)
        if (checkLocalWin(playerMark)) {
            updateStatus("You win!");
            gameActive = false;
            await handleGameOver("Player1", "win"); // เรียกฟังก์ชันจัดการจบเกม
            return;
        }
        if (isBoardFull()) {
            updateStatus("It's a Tie!");
            gameActive = false;
            await handleGameOver("Player1", "tie"); // เรียกฟังก์ชันจัดการจบเกม
            return;
        }

        // AI's Turn
        updateStatus("AI is thinking...");
        gameActive = false; // ป้องกันการคลิกระหว่าง AI คิด

        try {
            const response = await fetch('/api/play', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ board: currentBoard }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Network response was not ok');
            }

            const data = await response.json();
            currentBoard = data.new_board;
            updateBoardDisplay();
            updateStatus(data.message); // แสดงข้อความจาก API

            // Check game over status from API response
            if (data.winner === botMark) { // AI wins
                // gameActive ถูกตั้งเป็น false แล้วจาก API response หรือ logic ก่อนหน้า
                await handleGameOver("Player1", "loss"); // Player แพ้
            } else if (data.is_tie) { // Tie
                await handleGameOver("Player1", "tie");
            } else {
                // Game continues, Player's turn
                gameActive = true; // เปิดให้ผู้เล่นคลิกได้อีกครั้ง
            }
        } catch (error) {
            console.error("Error during AI turn:", error);
            updateStatus(`Error: ${error.message}. Please restart.`);
            gameActive = false; // ปิดเกมถ้ามีปัญหา
        }
    }

    // --- Helper Functions (เหมือนเดิม) ---
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
        updateStatus("Your turn (X)");
        // ไม่ต้อง createBoard() ซ้ำ ถ้า restartGame() เรียกมันแล้ว
        updateBoardDisplay(); // แค่อัปเดต UI ให้เป็นช่องว่าง
    }

    // --- Score Management ---
    async function updateScoreAPI(playerName, result) { // เปลี่ยนชื่อเล็กน้อย
        try {
            await fetch('/api/update_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_name: playerName, result: result }), // ใช้ result ที่รับมา
            });
            console.log(`Score update request sent for ${playerName} with result: ${result}`);
        } catch (error) {
            console.error(`Failed to update score for ${playerName}:`, error);
        }
    }

    async function fetchScores() {
        try {
            const response = await fetch('/api/get_scores');
            if (!response.ok) throw new Error('Failed to fetch scores');
            const data = await response.json(); // data.scores should be { "Player1": {stats}, "Bot": {stats} }

            const playerStats = data.scores["Player1"] || { score: 0, win_count: 0, win_streak: 0 };
            const botStats = data.scores["Bot"] || { score: 0, win_count: 0, win_streak: 0 };

            playerScoreElement.textContent = playerStats.score;
            botScoreElement.textContent = botStats.score;
            playerWinsElement.textContent = playerStats.win_count; // อัปเดต Win Count
            botWinsElement.textContent = botStats.win_count; // อัปเดต Win Count

            // อัปเดต Streak ถ้ามี Element
            // if (playerStreakElement) playerStreakElement.textContent = playerStats.win_streak;
            // if (botStreakElement) botStreakElement.textContent = botStats.win_streak;

        } catch (error) {
            console.error("Error fetching scores:", error);
            playerScoreElement.textContent = '-';
            botScoreElement.textContent = '-';
            playerWinsElement.textContent = '-'; // แสดง error
            botWinsElement.textContent = '-'; // แสดง error
        }
    }

    // --- Game Over Handling ---
    async function handleGameOver(playerName, result) {
        gameActive = false; // Ensure game stops
        console.log(`Game Over. Player: ${playerName}, Result: ${result}`);

        // Update scores based on result
        await updateScoreAPI(playerName, result);
        if (result === "loss") {
            // If Player1 lost, it means Bot won
            await updateScoreAPI("Bot", "win");
        } else if (result === "win") {
            // If Player1 won, it means Bot lost
            await updateScoreAPI("Bot", "loss");
        } else if (result === "tie") {
            // If it's a tie, update both (to reset streaks if necessary)
            await updateScoreAPI("Bot", "tie");
        }

        // Fetch and display updated scores
        await fetchScores();

        // Wait a bit then reset the board for a new game
        setTimeout(() => {
             console.log("Timeout finished, preparing for new game.");
             resetBoard(); // Reset board state
             gameActive = true; // Allow new game to start
             updateStatus("New Game! Your turn (X)");
        }, 3000); // 3 seconds delay
    }


    // --- Restart Game Completely ---
    async function restartGame() {
        console.log("Restarting game and resetting scores...");
        gameActive = false; // หยุดเกมชั่วคราว
        try {
            // 1. Reset scores on the server
            await fetch('/api/reset_scores', { method: 'POST' });
            console.log("Server scores reset request sent.");

            // 2. Fetch the reset scores (should be 0)
            await fetchScores(); // อัปเดต UI ให้เป็น 0
            console.log("Fetched reset scores.");

             // 3. Reset the local board state and UI
            resetBoard(); // รีเซ็ตค่าใน currentBoard และ UI board
            createBoard(); // สร้าง board ใหม่ (อาจจะไม่จำเป็นถ้า resetBoard ทำครบแล้ว)

            // 4. Set initial game state
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

    // --- Start Game ---
    createBoard(); // สร้าง Board ครั้งแรก
    fetchScores(); // ดึงคะแนนเริ่มต้นเมื่อโหลดหน้าเว็บ
    updateStatus("Your turn (X)"); // ตั้งค่าสถานะเริ่มต้น
});