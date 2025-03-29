const { DataTypes } = require('sequelize');
const { sequelize } = require('../config');

const User = sequelize.define('User', {
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  score: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  },
  winStreak: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  }
}, {
  tableName: 'users'
});

module.exports = User;