import random
from typing import List, Dict

from command import Command, Option
from player import Player, Color

suits = ["Harten", "Schoppen", "Klaver", "Ruiten"]
denoms = ["Aas", "Heer", "Vrouw", "Boer", "10", "9", "8", "7", "6", "5", "4", "3", "2"]


class Game(object):
    """description of class"""

    players: Dict[Color, Player]
    current_player: Player
    stock: List[str]
    number_of_cards: int

    def __init__(self, players=None):
        if players is None:
            players = [
                Player(Color.RED, "Rood"),
                Player(Color.BLUE, "Blauw"),
                Player(Color.YELLOW, "Geel"),
                Player(Color.GREEN, "Groen")]

        self.stock = []
        random.seed()
        self.number_of_cards = 0

        self.players = dict((player.color, player) for player in players)

        for player in self.players.values():
            player.options = [Option(Command.DEAL, None, "Delen")]
            player.message = "Wie begint er met delen?"

    def shuffle(self):
        deck = [x + " " + y for x in suits for y in denoms] + ["Joker" for _ in range(3)]
        self.stock = deck * 2

        for n in range(len(self.stock)):
            x = random.randint(0, len(self.stock) - n)
            value = self.stock[x]
            self.stock[x] = self.stock[n]
            self.stock[n] = value

    def deal(self, player_color):
        player = self.players[player_color]

        self.current_player = player

        if self.number_of_cards <= 2:
            self.shuffle()
            self.number_of_cards = 6
        else:
            self.number_of_cards -= 1

        for player in self.players.values():
            player.hand = self.stock[:self.number_of_cards]
            self.stock = self.stock[self.number_of_cards:]
            player.options = [Option(Command.CHANGECARD, [card], card) for card in player.hand]
            player.message = "Kies een kaart om te wisselen"
            player.selected_card = None
            player.card_is_changed = False

        return self.players

    def change_card(self, player_color, card):
        player = self.players[player_color]

        player.hand.remove(card)
        mate = self.mate(player)

        if mate.selected_card is None:
            player.selected_card = card
            player.message = "Wacht op je maat"
            player.options = [Option(Command.UNDOCARD, None, "Terug")]
            return self.players

        player.hand.append(mate.selected_card)
        mate.selected_card = None
        mate.hand.append(card)
        player.card_is_changed = True
        mate.card_is_changed = True
        mate.options.clear()
        player.options.clear()
        player.message = ""

        if all(player.card_is_changed for player in self.players.values()):
            self.next_turn()
        else:
            player.message = "Wacht op het andere team"
            mate.message = "wacht op het andere team"

        return self.players

    def play_card(self, player_color, card):
        player = self.players[player_color]

        player.hand.remove(card)
        player.selected_card = card
        player.options = [Option(Command.UNDOCARD, None, "Terug"), Option(Command.READY, None, "Klaar")]
        player.message = f"Je speelt {card}"

        for other in self.players.values():
            if other.color != player.color:
                other.message = f"{player.name} speelt {card}"

        return self.players

    def ready(self, player_color):
        player = self.players[player_color]

        player.options.clear()
        player.selected_card = None
        self.next_turn()

        return self.players

    def undo_card(self, player_color):
        player = self.players[player_color]

        player.hand.append(player.selected_card)
        player.selected_card = None

        if player.card_is_changed:
            self.turn()
        else:
            player.options = [Option(Command.CHANGECARD, [card], card) for card in player.hand]
            player.message = "Kies een kaart om te wisselen"

        return self.players

    def play_option(self, player, option):
        if option.command == Command.DEAL:
            return self.deal(player.color)
        elif option.command == Command.CHANGECARD:
            return self.change_card(player.color, option.args[0])
        elif option.command == Command.PLAYCARD:
            return self.play_card(player.color, option.args[0])
        elif option.command == Command.READY:
            return self.ready(player.color)
        elif option.command == Command.UNDOCARD:
            return self.undo_card(player.color)
        else:
            raise Exception(f"Unknown command {option.command}")

    def next_player(self, player):
        if player.color == Color.RED:
            return self.players[Color.BLUE]
        elif player.color == Color.BLUE:
            return self.players[Color.YELLOW]
        elif player.color == Color.YELLOW:
            return self.players[Color.GREEN]
        elif player.color == Color.GREEN:
            return self.players[Color.RED]
        else:
            raise Exception(f"Unknown color {player.Color}")

    def next_turn(self):
        self.current_player = self.next_player(self.current_player)
        self.turn()

    def turn(self):
        if len(self.current_player.hand) > 0:
            self.current_player.options = [Option(Command.PLAYCARD, [card], card) for card in self.current_player.hand]
            self.current_player.message = "Kies een kaart om te spelen"
            other_message = ""
        else:
            self.current_player.options = [Option(Command.DEAL, None, "Delen")]
            self.current_player.message = f"Jij bent aan de beurt om te delen."
            other_message = " om te delen"

        for player in self.players.values():
            if player.color != self.current_player.color:
                player.message = f"{self.current_player.name} is aan de beurt" + other_message

    def mate(self, player):
        if player.color == Color.RED:
            return self.players[Color.YELLOW]
        elif player.color == Color.BLUE:
            return self.players[Color.GREEN]
        elif player.color == Color.YELLOW:
            return self.players[Color.RED]
        elif player.color == Color.GREEN:
            return self.players[Color.BLUE]
        else:
            raise Exception(f"Unknown color {player.Color}")


if __name__ == "__main__":
    game = Game()

    # game.deal(Color.BLUE)
    # game.changeCard(Color.YELLOW, game.players[Color.YELLOW].hand[4])
    # game.changeCard(Color.RED, game.players[Color.RED].hand[2])
    # game.changeCard(Color.GREEN, game.players[Color.GREEN].hand[0])
    # game.changeCard(Color.BLUE, game.players[Color.BLUE].hand[5])
    # game.playCard(Color.YELLOW, game.players[Color.YELLOW].hand[1])
    # game.undoCard(Color.YELLOW)

    colors = [Color.BLUE, Color.YELLOW, Color.GREEN, Color.RED]

    for round in range(2):
        for deal in [6, 5, 4, 3, 2]:
            color = colors[0]
            print(color)
            game.deal(color)
            game.change_card(Color.YELLOW, game.players[Color.YELLOW].hand[deal - 1])
            game.change_card(Color.RED, game.players[Color.RED].hand[1])
            game.change_card(Color.GREEN, game.players[Color.GREEN].hand[0])
            game.change_card(Color.BLUE, game.players[Color.BLUE].hand[-1])

            colors = colors[1:] + [colors[0]]

            for turn in range(deal):
                for color in colors:
                    game.play_card(color, game.players[color].hand[0])
                    game.ready(color)

    for player in game.players.values():
        print(player.__dict__, end="\n\n")

    print(game.stock, end="\n\n")
