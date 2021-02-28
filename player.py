from enum import Enum
from cards import Card
from color import Color
from option import Option, OptionCode
from typing import List

import json


class StateCode(str, Enum):
    START = "start"
    PICK_COLOR = "pick_color"
    DEAL = "deal"
    DEAL_OTHER = "deal_other"
    SWAP_CARD = "swap_card"
    SWAP_CARD_OTHERS = "swap_card_others"
    PLAY_CARD = "play_card"
    PLAY_CARD_OTHER = "play_card_other"


class ErrorCode(str, Enum):
    NO_GAME = "no_game"
    UNKNOWN_CODE = "unknown_code"
    COLOR_ALREADY_CHOSEN = "color_already_chosen"
    OPTION_NOT_ALLOWED = "option_not_allowed"
    BAD_OPTION = "bad_option"


class PlayerState(object):
    def __init__(self, code, **kwargs):
        self.code = StateCode(code)
        self.args = kwargs


class PlayerError(object):
    def __init__(self, code, **kwargs):
        self.code = ErrorCode(code)
        self.args = kwargs


class OtherPlayer(object):
    def __init__(self, color, name):
        self.color = color
        self.name = name


class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Player(object):

    color: Color
    name: str
    game_code: int
    connected: bool
    hand: List[Card]
    options: List[Option]
    message: str
    state: PlayerState
    error: PlayerError
    swap_card: Card
    card_is_swapped: bool
    passed: bool
    others: List[OtherPlayer]
    current_player: OtherPlayer
    play_card: Card

    def __init__(self, color = None, name = None):
        self.color = color
        self.name = name
        self.game_code = None
        self.connected = True
        self.hand = []
        self.options = []
        self.message = "Even wachten"
        self.state = StateCode.START
        self.error = None
        self.swap_card = None
        self.card_is_swapped = False
        self.passed = False
        self.others = []
        self.current_player = None
        self.play_card = None

    def check_option(self, option):
        found_option = any(o.isOption(option) for o in self.options)

        if not found_option:
            self.message = f"{option.text} is niet toegestaan. " + self.message
            self.set_error(ErrorCode.OPTION_NOT_ALLOWED, option=option)
            
        return found_option

    def set_error(self, error_code, **kwargs):
        if error_code is not None:
            self.error = PlayerError(error_code, **kwargs)
        else:
            self.error = None

    def set_others(self, all_players):
        self.others = [OtherPlayer(p.color, p.name) for p in all_players if p.name != self.name or p.color != self.color]

    def set_current(self, current_player):
        self.current_player = OtherPlayer(current_player.color, current_player.name)

    def merge_from(self, other):
        self.color = other.color
        self.hand = other.hand
        self.options = other.options
        self.message = other.message
        self.state = other.state
        self.error = other.error
        self.swap_card = other.swap_card
        self.card_is_swapped = other.card_is_swapped
        self.passed = other.passed
        self.current_player = other.current_player
        self.play_card = other.play_card

    def get_json(self):
        return json.dumps(self.__dict__, cls=DictEncoder)


if __name__ == "__main__":
    player = Player(Color.BLUE, "Groen")
    player.options = [Option(OptionCode.NEW_GAME, "Nieuw spel", color='green'), Option(OptionCode.JOIN_GAME, "doe mee met een spel")]
    player.state = StateCode.PICK_COLOR
    print(player.__dict__)
    print(player.options[0].__dict__)
    print(player.get_json())
