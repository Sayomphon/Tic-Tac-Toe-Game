require('dotenv').config();
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: false, // ตั้งเป็น true เพื่อ debug ได้
});

module.exports = { sequelize };