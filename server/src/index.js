require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { sequelize } = require('./db/config'); // จะ import config มาจากไฟล์ config.js
const userRoutes = require('./routes/userRoutes');
const gameRoutes = require('./routes/gameRoutes');

const app = express();
const PORT = process.env.PORT || 4000;
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:5173';

// Middleware
app.use(cors({
  origin: FRONTEND_URL, // หรือจะใส่เป็น * ชั่วคราวก็ได้
  credentials: true
}));
app.use(express.json());

// ทดสอบ Route เบื้องต้น
app.get('/', (req, res) => {
  res.send('Hello from Tic Tac Toe Server!');
});

// ใช้งาน Routes
app.use('/api/users', userRoutes);
app.use('/api/game', gameRoutes);

// เชื่อมต่อ Database และเริ่มรัน Server
sequelize.sync({ alter: false }) // หรือ { force: false } ตามต้องการ
  .then(() => {
    console.log('Database synced successfully.');
    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
  })
  .catch(err => {
    console.error('Error syncing database:', err);
  });