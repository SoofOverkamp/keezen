import React from 'react'

export default function LoadingJoker({size}) {
    const style = {fontSize: `${size}pt`};
    console.log(style);
    return <div className="loading-joker"><span className="loading-joker-icon" style={style}>🃏</span></div>
}