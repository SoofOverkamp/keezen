import React, { useEffect, useState } from 'react';
import useWebsocket, { WebsocketStatus } from "./util/useWebsocket";
import LoadingJoker from "./LoadingJoker";
import LandingPage from "./LandingPage";
import Lobby from "./Lobby";

export const SiteState = {
    // Frontend only
    WAITING_FOR_WS: "waiting_for_ws",
    JOIN_LINK: "join_link",
    // Shared
    START: "start",
    JOIN_OTHERS: "join_others",
    PICK_COLOR: "pick_color",
    PICK_COLOR_OTHERS: "pick_color_others",
    FIRST_DEAL: "first_deal",
}

export const Commands = {
    NEW_GAME: "new_game",
    JOIN_GAME: "join_game",
    PICK_COLOR: "pick_color",
    DEAL: "deal",
    CHANGE_CARD: "change_card",
    PLAY_CARD: "play_card",
    READY: "ready",
    UNDO_CARD: "undo_card",
    PASS: "pass",
}

export default function StateRouter() {
    const [websocket, websocketStatus] = useWebsocket();

    const path = window.location.pathname.split("/");
    console.log(path);
    const initial_state = path[1] === "" ?
        { state: {code: SiteState.WAITING_FOR_WS }} :
        { state: {code: SiteState.JOIN_LINK, args: {game_code: parseInt(path[1]) }}};


    const [message, setMessage] = useState(initial_state);

    const {state: {code: state, args: state_args}, options} = message;

    useEffect(() => {
        if (websocketStatus === WebsocketStatus.CONNECTED && state === SiteState.JOIN_LINK) {
            websocket.send(JSON.stringify({
                code: Commands.JOIN_GAME,
                game_code: state_args.game_code,
                text: "Neem deel aan spel",   //TODO replace with option
            }))
        }
    }, [websocketStatus, message])

    useEffect(() => {
        if (state_args && state_args.game_code !== undefined && state_args.game_code !== null) {
            window.history.pushState(null, "", `/${state_args.game_code}`)
        }
        if (state_args && isNaN(state_args.game_code)) {
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
            return <LandingPage state={message}
                                newGame={() => websocket.send(JSON.stringify({
                                    code: Commands.NEW_GAME,
                                    text: "Begin nieuw spel",   //TODO replace with option
                                }))}/>
        case SiteState.JOIN_OTHERS:
        case SiteState.PICK_COLOR:
        case SiteState.PICK_COLOR_OTHERS:
        case SiteState.FIRST_DEAL:
            return <Lobby message={message}
                          pickColor={(color) => websocket.send(JSON.stringify({
                              code: Commands.PICK_COLOR,
                              text: "Kies kleur",   //TODO replace with option
                              color
                          }))}
                          deal={() => websocket.send(JSON.stringify({
                              code: Commands.DEAL,
                              text: "Deel",   //TODO replace with option
                          }))}/>
    }

    return `state: ${state}, wsstatus: ${websocketStatus}`
}