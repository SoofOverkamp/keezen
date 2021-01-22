import React, {useState} from 'react';
import { CardComponent } from "./Card";

export default function Hand({cards, play}) {
    const [selected, setSelected] = useState(null);

    return <div className="hand">
        {cards.map(c => <CardComponent value={c} play={() => play(c)}/>)}
    </div>
}