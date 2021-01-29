import React, { useState } from 'react';
import "./css/landingpage.css";

export default function LandingPage({ message, newGame, joinGame }) {
    const [showCodeInput, setShowCodeInput] = useState(false);
    const [code, setCode] = useState("");

    function handleCodeChange(e) {
        const value = e.target.value;
        if (value.length > 4) {
            return
        }
        if (value === "") {
            setCode(value);
        } else {
            const parsedCode = parseInt(e.target.value);
            if (isNaN(parsedCode)) {
                return
            }
            setCode(parsedCode)
        }
    }

                                                                                                                                                    
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
                       value={code}/>
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