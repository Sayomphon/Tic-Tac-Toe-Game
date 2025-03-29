import React, { useEffect, useState } from 'react'
import axios from 'axios'

const ScoreBoard = ({ API_BASE_URL }) => {
  const [scores, setScores] = useState([])

  const fetchScores = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/game/scoreboard`)
      setScores(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchScores()
  }, [])

  return (
    <div className="mt-4">
      <h2 className="font-bold mb-2">Scoreboard</h2>
      <button onClick={fetchScores} className="bg-gray-200 px-2 py-1 mb-2">
        Refresh
      </button>
      <ul>
        {scores.map(user => (
          <li key={user.id}>
            {user.username} - Score: {user.score}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ScoreBoard
