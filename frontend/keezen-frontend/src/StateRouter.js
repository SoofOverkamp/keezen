import React, { useEffect, useState } from 'react';
import useWebsocket, { WebsocketStatus } from "./util/useWebsocket";
import LoadingJoker from "./LoadingJoker";
import LandingPage from "./LandingPage";
import Lobby from "./Lobby";
import Game from "./Game";
import deck from "./img/deck.svg";

export const SiteState = {
    // Frontend only
    WAITING_FOR_WS: "waiting_for_ws",
    JOIN_LINK: "join_link",
    // Lobby
    START: "start",
    JOIN_OTHERS: "join_others",
    PICK_COLOR: "pick_color",
    PICK_COLOR_OTHERS: "pick_color_others",
    FIRST_DEAL: "first_deal",
    // Hand
    DEAL: "deal",
    DEAL_OTHER: "deal_other",
    SWAP_CARD: "swap_card",
    SWAP_CARD_PARTNER: "swap_card_partner",
    SWAP_CARD_OTHERS: "swap_card_others",
    PLAY_CARD: "play_card",
    PLAY_CARD_OTHER: "play_card_other",
    PLAYING_CARD: "playing_card",
    PLAYING_CARD_OTHER: "playing_card_other",

}

export const Commands = {
    NEW_GAME: "new_game",
    JOIN_GAME: "join_game",
    PICK_COLOR: "pick_color",
    DEAL: "deal",
    SWAP_CARD: "swap_card",
    PLAY_CARD: "play_card",
    READY: "ready",
    UNDO_CARD: "undo_card",
    PASS: "pass",
}

export default function StateRouter() {
    const [websocket, websocketStatus] = useWebsocket();

    const path = window.location.pathname;

    const path_code = path === "/" ?
        null :
        parseInt(path.split("/")[1]);

    console.log({path, path_code});
    const initial_state = path_code === null ?
        { state: { code: SiteState.WAITING_FOR_WS } } :
        { state: { code: SiteState.JOIN_LINK, args: { game_code: path_code } } };

    const send = websocketStatus === WebsocketStatus.CONNECTED ?
        (data) => websocket.send(JSON.stringify(data)) :
        (data) => console.error(`Cannot send: websocket is in state ${websocketStatus}, data:`, data);

    const [message, setMessage] = useState(initial_state);

    const { state: { code: state, args: state_args }, options } = message;

    useEffect(() => {
        if (websocketStatus === WebsocketStatus.CONNECTED && state === SiteState.JOIN_LINK) {
            send({
                code: Commands.JOIN_GAME,
                game_code: state_args.game_code,
                text: "Neem deel aan spel",
            })
        }
    }, [websocketStatus, message])

    useEffect(() => {
        if (state_args && state_args.game_code !== undefined && state_args.game_code !== null) {
            window.history.pushState(null, "", `/${state_args.game_code}`)
        }
        if (isNaN(path_code)) {
            window.history.pushState(null, "", "/")
        }
    }, [message])

    useEffect(() => {
            switch (websocketStatus) {
                case WebsocketStatus.RECONNECTING:
                case WebsocketStatus.CONNECTING:
                case WebsocketStatus.CONNECTED:
                    const handler = (event) => {
                        setMessage(JSON.parse(event.data))
                    };
                    websocket.addEventListener("message", handler)
                    return () => websocket.removeEventListener("message", handler)
            }
        }, [websocketStatus]
    )

    switch (websocketStatus) {
        case WebsocketStatus.DISCONNECTING:
        case WebsocketStatus.RECONNECTING:
        case WebsocketStatus.CONNECTING:
            return <LoadingJoker size={44}/>;
        case WebsocketStatus.ERROR:
        case WebsocketStatus.DISCONNECTED:
            return "Something went wrong :/";
        case WebsocketStatus.CONNECTED:
            break;
        default:
            console.error("Unknown websocketStatus", websocketStatus);
            return "Something went wrong :/";
    }

//    Websocket is now connected

    switch (state) {
        case SiteState.WAITING_FOR_WS:
            return <LoadingJoker size={44}/>
        case SiteState.START:
            return <LandingPage message={message}
                                newGame={() => send({
                                    code: Commands.NEW_GAME,
                                    text: "Begin nieuw spel",
                                })}
                                joinGame={(code) => send({
                                    code: Commands.JOIN_GAME,
                                    game_code: 3936,
                                    text: "Neem deel aan spel 3936",
                                })}/>
        case SiteState.JOIN_OTHERS:
        case SiteState.PICK_COLOR:
        case SiteState.PICK_COLOR_OTHERS:
        case SiteState.FIRST_DEAL:
            return <Lobby message={message}
                          pickColor={(color) => send({
                              code: Commands.PICK_COLOR,
                              text: "Kies kleur",
                              color
                          })}
                          deal={() => send({
                              code: Commands.DEAL,
                              text: "Deel", 
                          })}/>
        case SiteState.SWAP_CARD:
        case SiteState.SWAP_CARD_PARTNER:
        case SiteState.SWAP_CARD_OTHERS:
        case SiteState.PLAY_CARD:
        case SiteState.PLAY_CARD_OTHER:
        case SiteState.PLAYING_CARD:
        case SiteState.PLAYING_CARD_OTHER:
            return <Game message={message}
                         swapCard={(card) => send({
                             code: Commands.SWAP_CARD,
                             text: "Wissel kaart",
                             card,
                         })}
                         playCard={(card) => send({
                             code: Commands.PLAY_CARD,
                             text: "Speel kaart",
                             card,
                         })}
                         confirmPlay={() => send({
                             code: Commands.READY,
                             text: "Klaar/Bevestig kaart",
                         })}
                         undoPlay={() => send({
                             code: Commands.UNDO_CARD,
                             text: "Terug/Neem kaart terug",
                         })}/>
        case SiteState.DEAL:
            return <div className="row justify-content-center flex-md-column my-2">
                <h1>Klik om te delen</h1><br/>
                <div className="btn btn-link" onClick={() => send({
                    code: Commands.DEAL,
                    text: "Delen",
                })}>
                    <img src={deck} alt="kaartenstapel"/><br/><span>Delen</span>
                </div>
            </div>;
        case SiteState.DEAL_OTHER:
            return <h1>Wachten tot {state_args.other_player_name} heeft gedeeld</h1>
            
    }

    return `state: ${state}, wsstatus: ${websocketStatus}`
}