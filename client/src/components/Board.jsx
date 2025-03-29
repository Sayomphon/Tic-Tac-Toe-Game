import React from 'react'
import Square from './Square'

const Board = ({ board, onSquareClick }) => {
  return (
    <div className="grid grid-cols-3 gap-2 w-48">
      {board.map((cell, index) => (
        <Square
          key={index}
          value={cell}
          onClick={() => onSquareClick(index)}
        />
      ))}
    </div>
  )
}

export default Board
