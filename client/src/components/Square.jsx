import React from 'react'

const Square = ({ value, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="w-12 h-12 border flex items-center justify-center text-xl"
    >
      {value}
    </button>
  )
}

export default Square
