import React from "react";
import "./css/lobby.css"
import Colors from "./util/colors";
import deck from './img/deck.svg';
import { Commands } from "./StateRouter";

export default function Lobby({ message, pickColor, deal }) {
    const { color, options, state, game_code, others, name,...args } = message;
    const pickableColors = options.filter((o) => o.code === Commands.PICK_COLOR).map((o) => o.color);
    const circle_args = { state, myColor: color, myName: name, others, pickableColors, pickColor };
    const canDeal = options.find((o) => o.code === Commands.DEAL);
    return <div className="mt-4">
        <div className="row my-2">
            <h1>Je kan meedoen door naar <a href={`/${game_code}`}>{window.location.host}/{game_code}</a> te gaan
            </h1>
        </div>
        <div className="row justify-content-center my-2">
            <Circle color={Colors.RED} {...circle_args}/>
            <Circle color={Colors.YELLOW} {...circle_args}/>
            <Circle color={Colors.BLUE} {...circle_args}/>
            <Circle color={Colors.GREEN} {...circle_args}/>
        </div>
        {
            canDeal &&
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

function Circle({ color, myColor, myName, others, pickableColors, pickColor }) {
    const isMine = color === myColor;
    const playerInfo = isMine ?
        {color, name: myName} :
        others.find((o) => o.color === color);
    const isSelectable = pickableColors.includes(color);
    const isPicked = !isSelectable;
    const name = (playerInfo && playerInfo.name) || "";
    return <div className="col-2 flex-column">
        <div className={`color-pick 
                ${color} ${isPicked ? "selected" : ""} 
                ${isSelectable ? "selectable" : ""} 
                ${isMine ? "mine" : ""}`}
             onClick={() => isSelectable && pickColor(color)}
        />
        <h4>{name}</h4>
    </div>
}