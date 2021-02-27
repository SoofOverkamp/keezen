import React, { Fragment, useRef } from "react";
import Colors from "./util/colors";
import deck from './img/deck.svg';
import { Commands } from "./StateRouter";
import Pawn from "./Pawn";
import { useDebounce } from "./util/useDebounce";

export default function Lobby({ message, pickColor, deal, setName }) {
    const { color, options, state, game_code, others, name, ...args } = message;
    const pickableColors = options.filter((o) => o.code === Commands.PICK_COLOR).map((o) => o.color);

    const scheduleSetName = useDebounce(setName, 500)

    const circle_args = { state, myColor: color, myName: name, setMyName: scheduleSetName, others, pickableColors, pickColor };
    const canDeal = options.find((o) => o.code === Commands.DEAL);

    return <Fragment>
        <div className="top-bar">
            <span>Je kan meedoen door naar <a
                href={`/${game_code}`}>{window.location.origin}/{game_code}</a> te gaan</span>
        </div>
        <div className="content">
            <div className="container">
                <div className="row justify-content-center my-2">
                    <PawnWrapper color={Colors.RED} {...circle_args}/>
                    <PawnWrapper color={Colors.GREEN} {...circle_args}/>
                </div>
                <div className="row justify-content-center my2">
                    <PawnWrapper color={Colors.BLUE} {...circle_args}/>
                    <PawnWrapper color={Colors.YELLOW} {...circle_args}/>
                </div>
            </div>
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
    </Fragment>
}

function PawnWrapper({ color, myColor, myName, setMyName, others, pickableColors, pickColor }) {
    const isMine = color === myColor;
    const playerInfo = isMine ?
        { color, name: myName } :
        others.find((o) => o.color === color);
    const isSelectable = pickableColors.includes(color);
    const isSelected = !isSelectable;
    const name = (playerInfo && playerInfo.name) || "\u00a0";
    return <div className="col col-lg-3 col-md-4">
        <Pawn onClick={pickColor} size="large" {...{color, isMine, isSelectable, isSelected}} />
        {isMine ?
            <form className="color-pick-name">
                <input className="form-control"
                       type="text"
                       defaultValue={myName}
                       placeholder="Naam"
                       onChange={(e) => {
                           e.preventDefault();
                           setMyName(e.target.value);
                       }}/>
            </form> :
            <div className="color-pick-name">{name}</div>
        }
    </div>
}
