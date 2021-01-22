from enum import Enum
from color import Color
from cards import Card
import json


class OptionCode(str, Enum):
    NEW_GAME = "new_game"
    JOIN_GAME = "join_game"
    PICK_COLOR = "pick_color"
    DEAL = "deal"
    SWAP_CARD = "swap_card"
    PLAY_CARD = "play_card"
    READY = "ready"
    UNDO_CARD = "undo_card"
    PASS = "pass"


class Option(object):
    def __init__(self, code, text, game_code=None, color=None, card=None):
        self.code = OptionCode(code)
        self.text = text
        self.game_code = int(game_code) if game_code != None else None
        self.color = Color(color) if color != None else None
        self.card = card if isinstance(card, Card) else Card(card['suit'], card['denom']) if isinstance(card, dict) else None

    def isOption(self, other):
        # ignore text and game_code 
    
        return \
            self.code == other.code and \
            self.color == other.color and \
            self.card == other.card


if __name__ == "__main__":
    option = Option(OptionCode.NEW_GAME, "Nieuw spel", game_code=3)
    print(option)
    print(option.__dict__)
    print(json.dumps(option.__dict__))
    other = Option(OptionCode.NEW_GAME, "Start nog een spel", game_code=4)
    print(option.isOption(other))
    other = Option(OptionCode.NEW_GAME, "Doe maar gek", color='red')
    print(option.isOption(other))
    other = Option(OptionCode.SWAP_CARD, "Wissel kaart", card=Card("spades", "10"))