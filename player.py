from enum import Enum
from color import Color
from option import Option, OptionCode
import json


class StateCode(str, Enum):
    START = "start"
    JOIN_OTHERS = "join_others"
    PICK_COLOR = "pick_color"
    PICK_COLOR_OTHERS = "pick_color_others"
    FIRST_DEAL = "first_deal"
    DEAL = "deal"
    DEAL_OTHER = "deal_other"
    SWAP_CARD = "swap_card"
    SWAP_CARD_PARTNER = "swap_card_partner"
    SWAP_CARD_OTHERS = "swap_card_others"
    PLAY_CARD = "play_card"
    PLAY_CARD_OTHER = "play_card_other"
    PLAYING_CARD = "playing_card"
    PLAYING_CARD_OTHER = "playing_card_other"


class ErrorCode(str, Enum):
    UNKNOWN_CODE = "unknown_code"
    COLOR_ALREADY_CHOSEN = "color_already_chosen"
    OPTION_NOT_ALLOWED = "option_not_allowed"


class PlayerState(object):
    def __init__(self, code, **kwargs):
        self.code = StateCode(code)
        self.args = kwargs


class PlayerError(object):
    def __init__(self, code, **kwargs):
        self.code = ErrorCode(code)
        self.args = kwargs

class Player(object):
    def __init__(self, color = None, name = None):
        self.color = color
        self.name = name
        self.hand = []
        self.options = []
        self.message = "Even wachten"
        self.set_state(StateCode.START)
        self.error = None
        self.selected_card = None
        self.card_is_changed = False
        self.passed = False

    def check_option(self, option):
        found_option = any(o.isOption(option) for o in self.options)

        if not found_option:
            self.message = f"{option.text} is niet toegestaan. " + self.message
            self.set_error(ErrorCode.OPTION_NOT_ALLOWED, option=option)
            
        return found_option

    def set_state(self, state_code, **kwargs):
        self.state = PlayerState(state_code, **kwargs)

    def set_error(self, error_code, **kwargs):
        if error_code != None:
            self.error = PlayerError(error_code, **kwargs)
        else:
            self.error = None


class DogEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    player = Player(Color.BLUE, "Groen")
    player.options = [Option(OptionCode.NEW_GAME, "Nieuw spel", color='green'), Option(OptionCode.JOIN_GAME, "doe mee met een spel")]
    player.set_state(StateCode.PICK_COLOR, other_player_name="Rood")
    print(player.__dict__)
    print(player.options[0].__dict__)
    print(json.dumps(player.__dict__, cls=DogEncoder))
