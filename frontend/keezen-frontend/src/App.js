import './css/App.css';
import './css/SuitsFont.css';
import './css/Card.css';
import './css/bootstrap/bootstrap.css';
import './css/fontawesome.css';
import './css/regular.css';
import './css/solid.css';
import "./css/pawn.css";
import React from 'react';
import { DndProvider, TouchTransition, MouseTransition } from 'react-dnd-multi-backend'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { TouchBackend } from 'react-dnd-touch-backend'
import StateRouter from "./StateRouter";

export const HTML5toTouch = {
    backends: [
        {
            id: 'html5',
            backend: HTML5Backend,
            transition: MouseTransition,
        },
        {
            id: 'touch',
            backend: TouchBackend,
            options: { enableMouseEvents: true },
            preview: true,
            transition: TouchTransition,
        },
    ],
}
 

function App() {
    return <div className="App">
        <DndProvider options={HTML5toTouch}>
            <StateRouter/>
        </DndProvider>
    </div>
}


export default App;
