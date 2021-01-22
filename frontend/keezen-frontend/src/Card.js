import React from 'react';

export function CardComponent({value: {suit, denom}}, play) {
    console.log({suit, denom})
    return <div className={`playing-card card-${suit}`}>
        <div className="card-top">
            <span className="card-denom">{denomToChar(denom)}</span>
            <span className="card-suit">{suitToIcon(suit)}</span>
        </div>
        <button className="btn btn-success" onClick={play}><i className="fa fa-arrow-up"/></button>
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
        default:
            return denom
    }
}

export function fromString(s) {
    s = s.toLowerCase()
    if (s.toLowerCase() === Joker) {
        return {denom: "Joker", suit: null}
    }
    const split = s.split(" ")
    if (split.length !== 2) {
        console.error("Unknown card", s)
        return null
    }
    return {suit: split[0], denom: split[1]}
}

export const Joker = "joker"

export const Suits = {
    HEARTS: "harten",
    DIAMONDS: "ruiten",
    CLUBS: "klaver",
    SPADES: "schoppen"
}

export const Denoms = {
    ACE: "aas",
    KING: "koning",
    QUEEN: "vrouw",
    JACK: "boer",
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