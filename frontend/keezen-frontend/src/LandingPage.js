import React from 'react';
import "./css/landingpage.css";

export default function LandingPage({ message, newGame, joinGame }) {
    return <div className="landing-page row h-100 align-content-center justify-content-center flex-md-column">
        <button className="btn btn-primary mb-5" onClick={newGame}>Start een nieuw spel</button>
        {showCodeInput ?
            <form className="form-inline" onSubmit={(event) => {
                event.preventDefault();
                joinGame(code)
            }}>
                <input type="number"
                       className="form-control mx-2"
                       placeholder="1234"
                       onChange={handleCodeChange}
                       value={code}
                       autoFocus/>
                <button type="submit"
                        className="btn btn-secondary"
                        disabled={code === "" || code > 9999 || code < 1000}>
                    <i className="fa fa-arrow-right"/>
                </button>
            </form> :
            <button className="btn btn-secondary" onClick={() => setShowCodeInput(true)}>
                Doe mee met ander spel
            </button>}
    </div>;
}