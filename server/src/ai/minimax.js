/**
 * ตัวอย่างฟังก์ชัน Minimax (ย่อ/ง่ายๆ):
 * - board คือ array 9 ช่อง (string หรือ null)
 * - aiPlayer คือ 'O'
 * - huPlayer คือ 'X'
 */

function checkWin(board, player) {
    // ชุด index ที่จะชนะมี 8 รูปแบบ
    const winPatterns = [
      [0,1,2], [3,4,5], [6,7,8],
      [0,3,6], [1,4,7], [2,5,8],
      [0,4,8], [2,4,6],
    ];
    for (let pattern of winPatterns) {
      const [a,b,c] = pattern;
      if (board[a] === player && board[b] === player && board[c] === player) {
        return true;
      }
    }
    return false;
  }
  
  function checkDraw(board) {
    return board.every(cell => cell !== null && cell !== '');
  }
  
  function getAvailableMoves(board) {
    return board
      .map((val, idx) => (val === null || val === '') ? idx : null)
      .filter(idx => idx !== null);
  }
  
  function minimax(board, depth, isMaximizing, aiPlayer, huPlayer) {
    // เช็ค terminal state
    if (checkWin(board, huPlayer)) {
      return { score: -10 + depth };
    } else if (checkWin(board, aiPlayer)) {
      return { score: 10 - depth };
    } else if (checkDraw(board)) {
      return { score: 0 };
    }
  
    // ถ้าเป็นเทิร์น AI
    if (isMaximizing) {
      let best = { score: -Infinity };
      for (let move of getAvailableMoves(board)) {
        board[move] = aiPlayer;
        let result = minimax(board, depth + 1, false, aiPlayer, huPlayer);
        board[move] = null;
        if (result.score > best.score) {
          best = { score: result.score, index: move };
        }
      }
      return best;
    }
    // ถ้าเป็นเทิร์นผู้เล่น
    else {
      let best = { score: Infinity };
      for (let move of getAvailableMoves(board)) {
        board[move] = huPlayer;
        let result = minimax(board, depth + 1, true, aiPlayer, huPlayer);
        board[move] = null;
        if (result.score < best.score) {
          best = { score: result.score, index: move };
        }
      }
      return best;
    }
  }
  
  function calculateBestMove(board, aiPlayer = 'O', huPlayer = 'X') {
    // เรียกใช้ minimax
    const bestMove = minimax(board, 0, true, aiPlayer, huPlayer);
    return bestMove.index; 
  }
  
  module.exports = { calculateBestMove, checkWin, checkDraw };