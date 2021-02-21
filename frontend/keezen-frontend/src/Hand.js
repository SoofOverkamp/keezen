import React, { useState } from 'react';
import { Card } from "./Card";

export default function Hand({ cards, play }) {
    const [selected, setSelected] = useState(null);

    const deselectAndPlay = (c) => {
        if (play !== null) {
            if (selected === c.uid) {
                setSelected(null)
            }
            play(c)
        }
    }

    return <div className="bottom-bar hand">
        <div className="container">
            <div className="row m-auto">
                {cards.map((c) => <div key={c.uid} className="col-2">
                    <Card value={c}
                          animate={play !== null}
                          play={() => deselectAndPlay(c)}
                          select={selected === c.uid ? () => setSelected(null) : () => setSelected(c.uid)}
                          selected={selected === c.uid}/></div>)}
            </div>
        </div>
    </div>
}
