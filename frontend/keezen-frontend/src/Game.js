import React, { Fragment } from 'react';
import Hand from "./Hand";
import { SiteState } from "./StateRouter";
import { Card } from "./Card";
import { colorToText } from "./util/colors";
import { useDrop } from 'react-dnd'
import "./css/game.css"

export default function Game({ message, swapCard, playCard, confirmPlay, undoPlay, skipTurn }) {
    console.log(message);

    const { hand, state, current_player, play_card, swap_card, name, color } = message;

    let play = null;
    let card = null;
    let undo = null;
    let text;
    switch (state) {
        case SiteState.SWAP_CARD:
            play = swapCard;
            if (swap_card) {
                card = swap_card;
                undo = undoPlay;
                text = "Wacht op een kaart van je partner";
            } else {
                text = "Kies een kaart voor je partner";
            }
            break;
        case SiteState.SWAP_CARD_OTHERS:
            text = "Wacht op het andere team";
            break;
        case SiteState.PLAY_CARD:
            play = playCard;
            card = play_card;
            text = "Kies een kaart om te spelen";
            if (play_card) {
                undo = undoPlay
            }
            break;
        case SiteState.PLAY_CARD_OTHER:
            card = play_card;
            text = `${colorToText(current_player.color)} is aan de beurt`;
            break;
    }

    const [{}, dropPlay] = useDrop({
        accept: "card",
        canDrop: (item) => item && item.card && (!card || card != item.card),
        drop: () => play && play(),
    });

    const [{}, dropUndo] = useDrop({
        accept: "card",
        canDrop: (item) => item && item.card && card && card == item.card,
        drop: () => undo && undo(),
    });

    return <div className="game">
        <header className={`name ${color}`}>
            {name || "your name"}
        </header>
        <div ref={dropPlay}>
            <h1>{text}</h1>
            {card &&
            <Card value={card} play={undo}/>
            }
            {card && play_card && state === SiteState.PLAY_CARD &&
            <button className="btn btn-success" onClick={confirmPlay}>Volgende speler</button>
            }
            {card && (state === SiteState.PLAY_CARD || state === SiteState.SWAP_CARD) &&
            <button className="btn btn-secondary" onClick={undoPlay}>Neem terug</button>
            }
            <br/>
            <div className="main row h-100 align-content-center justify-content-center flex-md-column"/>
            {state === SiteState.PLAY_CARD &&
            <button className="btn btn-primary" onClick={skipTurn}>Pas</button>
            }
        </div>
        <div ref={dropUndo}>
            <Hand cards={hand} play={play}/>
        </div>
    </div>;
}