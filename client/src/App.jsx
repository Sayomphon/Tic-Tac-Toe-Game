import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Board from './components/Board'
import ScoreBoard from './components/ScoreBoard'

function App() {
  const [username, setUsername] = useState('')
  const [user, setUser] = useState(null)
  const [board, setBoard] = useState(Array(9).fill(null))
  const [gameStatus, setGameStatus] = useState('READY') // READY, ONGOING, PLAYER_WIN, AI_WIN, DRAW

  // Backend base URL (ปรับตามจริง ถ้า Deploy ก็เปลี่ยน URL)
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:4000/api'

  const handleLogin = async () => {
    if (!username) return
    try {
      const res = await axios.post(`${API_BASE_URL}/users`, { username })
      setUser(res.data)
      setGameStatus('ONGOING')
    } catch (err) {
      console.error(err)
    }
  }

  const handleSquareClick = async (index) => {
    if (!user) return
    if (board[index] !== null) return // ช่องไม่ว่าง

    try {
      const res = await axios.post(`${API_BASE_URL}/game/move`, {
        userId: user.id,
        board,
        playerMoveIndex: index
      })
      setBoard(res.data.board)
      setGameStatus(res.data.status)
      if (res.data.user) {
        setUser(res.data.user) // อัปเดตคะแนน
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleReset = () => {
    // เริ่มใหม่
    setBoard(Array(9).fill(null))
    setGameStatus('ONGOING')
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Tic Tac Toe with AI</h1>

      {!user && (
        <div className="mb-4">
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border p-2 mr-2"
          />
          <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2">
            Start Game
          </button>
        </div>
      )}

      {user && (
        <div className="mb-4">
          <p>Welcome, {user.username}!</p>
          <p>Score: {user.score}</p>
          <p>WinStreak: {user.winStreak}</p>
        </div>
      )}

      {gameStatus !== 'READY' && (
        <Board board={board} onSquareClick={handleSquareClick} />
      )}

      <div className="mt-4">
        {gameStatus === 'PLAYER_WIN' && <p>You Win!</p>}
        {gameStatus === 'AI_WIN' && <p>You Lose!</p>}
        {gameStatus === 'DRAW' && <p>Draw!</p>}
        {(gameStatus === 'PLAYER_WIN' || gameStatus === 'AI_WIN' || gameStatus === 'DRAW') && (
          <button onClick={handleReset} className="bg-gray-300 px-4 py-2 mt-2">
            Play Again
          </button>
        )}
      </div>

      <ScoreBoard API_BASE_URL={API_BASE_URL} />
    </div>
  )
}

export default App
