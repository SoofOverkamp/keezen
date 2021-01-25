import React, { Fragment } from 'react';
import Hand from "./Hand";
import { SiteState } from "./StateRouter";
import { Card } from "./Card";

export default function Game({ message, swapCard, playCard, confirmPlay, undoPlay }) {
    console.log(message);
    const { hand, state: { code: state, args: {other_player_name, card} }, selected_card } = message;

    let play = null;
    let text;
    switch (state) {
        case SiteState.SWAP_CARD:
            play = swapCard;
            text = "Kies een kaart voor je partner";
            break;
        case SiteState.SWAP_CARD_PARTNER:
            text = "Wacht op een kaart van je partner";
            break;
        case SiteState.SWAP_CARD_OTHERS:
            text = "Wacht op het andere team";
            break;
        case SiteState.PLAY_CARD:
            play = playCard;
            text = "Kies een kaart om te spelen";
            break;
        case SiteState.PLAYING_CARD:
            text = "Bevestig kaart keuze";
            break;
        case SiteState.PLAY_CARD_OTHER:
            text = `${other_player_name} is een kaart aan het kiezen`;
            break;
        case SiteState.PLAYING_CARD_OTHER:
            text = `${other_player_name} speelt kaart`;
            break;

    }


    return <Fragment>
        <h1>{text}</h1>
        {card || selected_card ?
            <Card value={card || selected_card}/> : null
        }
        {state === SiteState.PLAYING_CARD ?
                <button className="btn btn-primary" onClick={confirmPlay}>Bevestig</button> : null
        }
        {state === SiteState.SWAP_CARD_PARTNER || state === SiteState.PLAYING_CARD ?
            <button className="btn btn-danger" onClick={undoPlay}>Neem terug</button> : null
        }
        <Hand cards={hand} play={play}/>
    </Fragment>;
}