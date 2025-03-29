const express = require('express');
const User = require('../db/models/User');
const router = express.Router();

/**
 * POST /api/users
 * รับ username -> ถ้ายังไม่มีใน DB ก็สร้างใหม่ -> ส่งข้อมูล user กลับ
 */
router.post('/', async (req, res) => {
  try {
    const { username } = req.body;
    if (!username) {
      return res.status(400).json({ error: 'Username is required' });
    }

    // หา User ใน DB
    let user = await User.findOne({ where: { username } });
    if (!user) {
      user = await User.create({ username });
    }

    res.json(user);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;