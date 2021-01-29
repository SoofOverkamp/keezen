import React from 'react';
import "./css/landingpage.css";

export default function LandingPage({ message, newGame, joinGame }) {
    return <div className="landing-page row h-100 align-content-center justify-content-center flex-md-column">
        <button className="btn btn-primary mb-5" onClick={newGame}>Begin met spelen</button>
        <button className="btn btn-secondary" onClick={joinGame}>Doe mee met ander spel</button>
    </div>;
}