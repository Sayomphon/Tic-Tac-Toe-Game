const { DataTypes } = require('sequelize');
const { sequelize } = require('../config');
const User = require('./User');

const Score = sequelize.define('Score', {
  points: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  }
}, {
  tableName: 'scores'
});

// ตัวอย่างการตั้ง Association
User.hasOne(Score, {
  foreignKey: 'userId',
  onDelete: 'CASCADE'
});
Score.belongsTo(User, {
  foreignKey: 'userId'
});

module.exports = Score;