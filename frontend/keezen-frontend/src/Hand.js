import React, { useState } from 'react';
import { Card } from "./Card";

export default function Hand({ cards, play }) {
    const [selected, setSelected] = useState(null);

    return <div className="bottom-bar hand">
        <div className="container">
            <div className="row m-auto">
                {cards.map((c, i) => <div className="col-2">
                    <Card value={c}
                          animate={play !== null}
                          play={play === null ? null : (() => play(c))}
                          select={selected === i ? () => setSelected(null) : () => setSelected(i)}
                          selected={selected === i}/></div>)}
            </div>
        </div>
    </div>
}
