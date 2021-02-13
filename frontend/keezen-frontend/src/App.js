import './css/App.css';
import './css/SuitsFont.css';
import './css/Card.css';
import './css/bootstrap/bootstrap.css';
import './css/fontawesome.css';
import './css/regular.css';
import './css/solid.css';
import { Denoms, Suits } from "./Card";
import Hand from "./Hand";
import StateRouter from "./StateRouter";

function App() {
    return <div className="App">
        <StateRouter/>
        {/*<Hand cards={[*/}
        {/*    { suit: Suits.DIAMONDS, denom: Denoms.ACE },*/}
        {/*    { suit: Suits.CLUBS, denom: Denoms.D8 },*/}
        {/*    { suit: Suits.CLUBS, denom: Denoms.D8 },*/}
        {/*    { suit: Suits.CLUBS, denom: Denoms.D8 },*/}
        {/*    { suit: Suits.CLUBS, denom: Denoms.D8 },*/}
        {/*]}/>*/}
    </div>
}


export default App;
