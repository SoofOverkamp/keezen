import React from 'react';
import "./css/landingpage.css";

export default function LandingPage({ state, newGame }) {
    return <div className="landing-page row h-100 align-content-center justify-content-center">
        <button className="btn btn-primary mb-5" onClick={newGame}>Begin met spelen</button>
    </div>;
}