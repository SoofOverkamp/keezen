import React, { Fragment } from 'react';
import Hand from "./Hand";
import { SiteState } from "./StateRouter";
import { Card } from "./Card";
import { colorToText } from "./util/colors";

export default function Game({ message, swapCard, playCard, confirmPlay, undoPlay, skipTurn }) {
    console.log(message);
    const { hand, state, current_player, play_card, swap_card } = message;

    let play = null;
    let card = null;
    let text;
    switch (state) {
        case SiteState.SWAP_CARD:
            play = swapCard;
            if (swap_card) {
                card = swap_card;
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
            break;
        case SiteState.PLAY_CARD_OTHER:
            card = play_card;
            text = `${colorToText(current_player.color)} is aan de beurt`;
            break;
    }


    return <Fragment>
        <div className="top-bar">{text}</div>
            <div className="container">
                {card &&
                <Card value={card}/>
                }
                {card && play_card && state === SiteState.PLAY_CARD &&
                <button className="btn btn-success" onClick={confirmPlay}>Volgende speler</button>
                }
                {card && (state === SiteState.PLAY_CARD || state === SiteState.SWAP_CARD) &&
                <button className="btn btn-secondary" onClick={undoPlay}>Neem terug</button>
                }
                <br/>
                {state === SiteState.PLAY_CARD &&
                <button className="btn btn-primary" onClick={skipTurn}>Pas</button>
                }
            </div>
        <Hand cards={hand} play={play}/>
    </Fragment>;
}