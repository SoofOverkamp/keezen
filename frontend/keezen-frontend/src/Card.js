import React from 'react';

export function Card({value: {suit, denom}, play, animate, selected, select}) {
    return <div className={`playing-card card-${suit || Joker} ${animate ? "animate" : ""} ${selected ? "selected" : ""}`}
                onClick={select || (() => {})}>
        <div className="card-top">
            <span className="card-denom">{denomToChar(denom)}</span>
            <span className="card-suit">{suitToIcon(suit)}</span>
        </div>
        {play && <button className="btn btn-success"  onClick={(event) => {
            event.preventDefault();
            event.stopPropagation();
            play(event);
        }}><i className="fa fa-arrow-up"/></button>}
    </div>;
}

function suitToIcon(suit) {
    let icon = null
    switch (suit) {
        case Suits.SPADES:
            icon = "icon-spades"
            break
        case Suits.CLUBS:
            icon = "icon-clubs"
            break
        case Suits.HEARTS:
            icon = "icon-hearts"
            break
        case Suits.DIAMONDS:
            icon = "icon-diamonds"
            break
    }
    return icon && <i className={icon}/>
}

function denomToChar(denom) {
    switch (denom) {
        case Denoms.ACE:
            return "A"
        case Denoms.KING:
            return "K"
        case Denoms.QUEEN:
            return "V"
        case Denoms.JACK:
            return "J"
        case Joker:
            return "Joker"
        default:
            return denom
    }
}
export const Joker = "joker"

export const Suits = {
    HEARTS: "hearts",
    DIAMONDS: "diamonds",
    CLUBS: "clubs",
    SPADES: "spades"
}

export const Denoms = {
    ACE: "ace",
    KING: "king",
    QUEEN: "queen",
    JACK: "jack",
    D10: "10",
    D9: "9",
    D8: "8",
    D7: "7",
    D6: "6",
    D5: "5",
    D4: "4",
    D3: "3",
    D2: "2",
}