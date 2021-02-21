import React, { Fragment } from 'react';
import Hand from "./Hand";
import { SiteState } from "./StateRouter";
import { Card } from "./Card";
import { colorToText } from "./util/colors";
import "./css/Game.css"
import Pawn from "./Pawn";
import { useDebounce } from "./util/useDebounce";
import deck from "./img/deck.svg";

export default function Game({ message, swapCard, playCard, confirmPlay, undoPlay, skipTurn, deal, setName }) {
    const { color, name, hand, state, current_player, play_card, swap_card } = message;

    const scheduleSetName = useDebounce(setName, 500)

    const currentPlayerName = current_player.name && current_player.name !== "" ?
        current_player.name : colorToText(current_player.color);

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
            text = `${currentPlayerName} is aan de beurt`;
            break;
        case SiteState.DEAL:
            text = "Klik op de stapel om te delen";
            break;
        case SiteState.DEAL_OTHER:
            text = `Wachten tot ${currentPlayerName} heeft gedeeld`;
            break;
    }


    return <Fragment>
        <div className="top-bar">
            <div className="row">
                <div className="col-2"/>
                <div className="col-8">{text}</div>
                <div className="col-2">
                    <Pawn color={color} isSelected={true} isMine={true} isSelectable={false} size="medium"/>
                    <form className="status-name">
                        <input className="form-control"
                               type="text"
                               defaultValue={name}
                               placeholder="Vul een naam in"
                               onChange={(e) => {
                                   e.preventDefault();
                                   scheduleSetName(e.target.value);
                               }}/>
                    </form>
                </div>
            </div>
        </div>
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
        {(state !== SiteState.DEAL && state !== SiteState.DEAL_OTHER) &&
            <Hand cards={hand} play={play}/>
        }
        {state === SiteState.DEAL &&
            <div className="row justify-content-center flex-md-column my-2">
                <div className="btn btn-link" onClick={deal}>
                    <img src={deck} alt="kaartenstapel"/><br/><span>Delen</span>
                </div>
            </div>
        }
    </Fragment>;
}