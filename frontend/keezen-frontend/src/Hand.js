import React, { useState } from 'react';
import { Card } from "./Card";

export default function Hand({ cards, play }) {
    const [selected, setSelected] = useState(null);

    return <div className="hand">
        {cards.map((c, i) => <Card value={c}
                                   animate={play !== null}
                                   play={play === null ? null : (() => play(c))}
                                   select={selected === i ? () => setSelected(null) : () => setSelected(i)}
                                   selected={selected === i}/>)}
    </div>
}
