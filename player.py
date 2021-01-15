from enum import Enum
from command import Option
import json
import jsonpickle


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    YELLOW = "yellow"
    GREEN = "green"

    def __getstate__(self):
        return "hallo"

    def __setstate__(state):
        return Color(state)


class Player(object):
    def __init__(self, color = None, name = None):
        self.color = color
        self.name = name
        self.hand = []
        self.options = []
        self.message = "Even wachten"
        self.selected_card = None
        self.card_is_changed = False

    def check_option(self, option):
        found_option = any(option.command == o.command and o.check_args(option) for o in self.options)

        if not found_option:
            self.message = f"{option.text} is niet toegestaan. " + self.message
            
        return found_option


class DogEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    player = Player(Color.BLUE, "Groen")
    player.options = [Option("newgame", None, "text")]
    print(player)
    print(player.__dict__)
    print(json.dumps(player, cls=DogEncoder))
    # print(json.dumps(player))
    print(jsonpickle.encode(player))
