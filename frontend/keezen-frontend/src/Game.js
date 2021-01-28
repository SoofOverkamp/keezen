import React, { Fragment } from 'react';
import Hand from "./Hand";
import { SiteState } from "./StateRouter";
import { Card } from "./Card";

export default function Game({ message, swapCard, playCard, confirmPlay, undoPlay }) {
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
            text = `${current_player.color}(${current_player.name}) is een kaart aan het kiezen`;
            break;
    }


    return <Fragment>
        <h1>{text}</h1>
        {card &&
        <Card value={card}/>
        }
        {card && play_card &&
        <button className="btn btn-primary" onClick={confirmPlay}>Bevestig</button>
        }
        {card &&
        <button className="btn btn-danger" onClick={undoPlay}>Neem terug</button>
        }
        <Hand cards={hand} play={play}/>
    </Fragment>;
}