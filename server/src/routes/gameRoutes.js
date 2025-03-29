const express = require('express');
const User = require('../db/models/User');
const { calculateBestMove, checkWin, checkDraw } = require('../ai/minimax');

const router = express.Router();

/**
 * POST /api/game/move
 * body: { userId, board, playerMoveIndex }
 * - board เป็น array 9 ช่อง เช่น [ 'X', null, ... ]
 * - playerMoveIndex คือช่องที่ผู้เล่นเลือกเดิน (0-8)
 * - เราให้ AI เป็น 'O', ผู้เล่นเป็น 'X'
 */
router.post('/move', async (req, res) => {
  try {
    const { userId, board, playerMoveIndex } = req.body;
    if (!userId || !board || playerMoveIndex === undefined) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // 1) อัปเดต board ด้วยการเดินของผู้เล่น
    board[playerMoveIndex] = 'X';

    // 2) เช็คผลผู้เล่นชนะ?
    if (checkWin(board, 'X')) {
      // อัปเดต score
      const user = await updateScore(userId, true);
      return res.json({
        board,
        status: 'PLAYER_WIN',
        user
      });
    }
    if (checkDraw(board)) {
      return res.json({
        board,
        status: 'DRAW'
      });
    }

    // 3) ถ้าผู้เล่นยังไม่ชนะ ให้ AI เดิน
    const bestMoveIndex = calculateBestMove(board, 'O', 'X');
    if (bestMoveIndex !== undefined) {
      board[bestMoveIndex] = 'O';
    }

    // 4) เช็คผล AI ชนะ?
    if (checkWin(board, 'O')) {
      // อัปเดต score ของ player (กรณีแพ้ -1)
      const user = await updateScore(userId, false);
      return res.json({
        board,
        status: 'AI_WIN',
        user
      });
    }

    // 5) เช็คเสมอ
    if (checkDraw(board)) {
      return res.json({
        board,
        status: 'DRAW'
      });
    }

    // 6) ถ้ายังไม่จบเกม
    return res.json({
      board,
      status: 'ONGOING'
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/game/scoreboard
 * - ดึงข้อมูลผู้เล่นทั้งหมด เรียงตามคะแนนมาก -> น้อย
 */
router.get('/scoreboard', async (req, res) => {
  try {
    const users = await User.findAll({
      order: [['score', 'DESC']]
    });
    res.json(users);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});


/**
 * ฟังก์ชัน updateScore
 * - ถ้าชนะ: +1, winStreak +1
 * - ถ้าแพ้: -1, winStreak = 0
 * - ถ้าชนะ 3 ครั้งติด -> บวกคะแนนพิเศษ +1
 */
async function updateScore(userId, isWin) {
  let user = await User.findByPk(userId);
  if (!user) return null;

  if (isWin) {
    user.winStreak += 1;
    user.score += 1;
    if (user.winStreak >= 3) {
      user.score += 1; // +1 bonus
      user.winStreak = 0; // reset streak
    }
  } else {
    // แพ้
    user.score -= 1;
    user.winStreak = 0;
  }

  await user.save();
  return user;
}

module.exports = router;