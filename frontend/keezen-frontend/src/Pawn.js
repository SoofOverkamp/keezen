import React from "react";

export default function Pawn({color, isSelected, isSelectable, isMine, onClick, size}) {
    return <div className={`pawn
                ${size} 
                ${color} 
                ${isSelected ? "selected" : ""} 
                ${isSelectable ? "selectable" : ""} 
                ${isMine ? "mine" : ""}`}
             onClick={() => isSelectable && onClick(color)}>
        </div>
}