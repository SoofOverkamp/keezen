from enum import Enum
import json

class Command(str, Enum):
    NEWGAME = "newgame"
    JOINGAME = "joingame"
    PICKCOLOR = "pickcolor"
    DEAL = "deal"
    CHANGECARD = "changecard"
    PLAYCARD = "playcard"
    READY = "ready"
    UNDOCARD = "undocard"
    PASS = "pass"

class Option(object):
    def __init__(self, command, args=None, text=None):
        self.command = command # Command(command)
        self.args = args
        self.text = text

    def checkArg(self, expectedArg, givenArg):
        return expectedArg == "#" or expectedArg == givenArg

    def checkArgs(self, other):
        if self.args == other.args:
            return True

        if self.args == None or len(self.args) == 0 or len(self.args) != len(other.args):
            return False

        return all(self.checkArg(expected, given) for (expected, given) in zip(self.args, other.args))

if __name__ == "__main__":
   option = Option("newgame")
   print(option)
   print(option.__dict__)
   print(json.dumps(option))
