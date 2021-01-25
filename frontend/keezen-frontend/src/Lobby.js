import React from "react";
import "./css/lobby.css"
import Colors from "./util/colors";
import deck from './img/deck.svg';
import { SiteState } from "./StateRouter";

export default function Lobby({ message, pickColor, deal }) {
    const { color, options, state: { code: state, args: { game_code, ...state_args } } } = message;
    const freeColors = (options && options.map((o) => o.color)) || [];
    const circle_args = { state, myColor: color, freeColors, pickColor };
    return <div className="mt-4">
        {
            state === SiteState.JOIN_OTHERS &&
            <div className="row my-2">
                <h1>Je kan meedoen door naar <a href={`/${game_code}`}>{window.location.host}/{game_code}</a> te gaan
                </h1>
            </div>
        }{/*<hr/>*/}{
            state !== SiteState.JOIN_OTHERS &&
            <div className="row justify-content-center my-2">
                <Circle color={Colors.RED} {...circle_args}/>
                <Circle color={Colors.YELLOW} {...circle_args}/>
                <Circle color={Colors.BLUE} {...circle_args}/>
                <Circle color={Colors.GREEN} {...circle_args}/>
            </div>
        }{
            state === SiteState.FIRST_DEAL &&
            <div className="row justify-content-center my-2">
                <div className="btn btn-link" onClick={deal}>
                    <img src={deck} alt="kaartenstapel"/>
                    <br/>
                    <span>Delen</span>
                </div>
            </div>
        }
    </div>
}

function Circle({ state, color, myColor, freeColors, pickColor }) {
    const isMine = color === myColor;
    const isSelectable = freeColors.includes(color)
    const isPicked = state === SiteState.PICK_COLOR && !isSelectable;
    return <div className="col-2">
        <div className={`color-pick 
                ${color} ${isPicked ? "selected" : ""} 
                ${isSelectable ? "selectable" : ""} 
                ${isMine ? "mine" : ""}`}
            onClick={() => isSelectable && pickColor(color)}
        />
    </div>
}