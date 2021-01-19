import random
from typing import List, Dict

from color import Color
from cards import Card, shuffle
from option import OptionCode, Option
from player import Player, StateCode, ErrorCode


class Game(object):
    """description of class"""

    players: Dict[Color, Player]
    current_player: Player
    current_dealer: Player
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
            player.options = [Option(OptionCode.DEAL, "Delen")]
            player.message = "Wie begint er met delen?"
            player.set_state(StateCode.FIRST_DEAL)

    def deal(self, player_color):
        player = self.players[player_color]

        self.current_player = player
        self.current_dealer = player

        if self.number_of_cards <= 2:
            self.stock = shuffle(2)
            self.number_of_cards = 6
        else:
            self.number_of_cards -= 1

        for player in self.players.values():
            player.hand = self.stock[:self.number_of_cards]
            self.stock = self.stock[self.number_of_cards:]
            player.options = [Option(OptionCode.SWAP_CARD, card.denom, card=card) for card in player.hand]
            player.message = "Kies een kaart om te wisselen"
            player.set_state(StateCode.SWAP_CARD)
            player.selected_card = None
            player.card_is_changed = False
            player.passed = False

        return self.players

    def change_card(self, player_color, card):
        player = self.players[player_color]

        player.hand.remove(card)
        partner = self.partner(player)

        if partner.selected_card is None:
            player.selected_card = card
            player.message = "Wacht op je maat"
            player.set_state(StateCode.SWAP_CARD_PARTNER)
            player.options = [Option(OptionCode.UNDO_CARD, "Terug")]
            return self.players

        player.hand.append(partner.selected_card)
        partner.selected_card = None
        partner.hand.append(card)
        player.card_is_changed = True
        partner.card_is_changed = True
        partner.options.clear()
        player.options.clear()
        player.message = ""

        if all(player.card_is_changed for player in self.players.values()):
            self.next_turn()
        else:
            player.message = "Wacht op het andere team"
            player.set_state(StateCode.SWAP_CARD_OTHERS)
            partner.message = "wacht op het andere team"
            partner.set_state(StateCode.SWAP_CARD_OTHERS)

        return self.players

    def play_card(self, player_color, card):
        player = self.players[player_color]

        player.hand.remove(card)
        player.selected_card = card
        player.options = [Option(OptionCode.UNDO_CARD, "Terug"), Option(OptionCode.READY, "Klaar")]
        player.message = f"Je speelt {card}"
        player.set_state(StateCode.PLAYING_CARD, card=card)

        for other in self.players.values():
            if other.color != player.color:
                other.message = f"{player.name} speelt {card}"
                other.set_state(StateCode.PLAYING_CARD_OTHER, card=card, other_player_name=player.name)

        return self.players

    def drop_cards(self, player_color):
        player = self.players[player_color]

        player.hand = []
        player.options = []
        player.passed = True
        self.next_turn()

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
            player.options = [Option(OptionCode.SWAP_CARD, card.denom, card=card) for card in player.hand]
            player.message = "Kies een kaart om te wisselen"
            player.set_state(StateCode.SWAP_CARD)

        return self.players

    def play_option(self, player, option):
        if option.code == OptionCode.DEAL:
            return self.deal(player.color)
        elif option.code == OptionCode.SWAP_CARD:
            return self.change_card(player.color, option.card)
        elif option.code == OptionCode.PLAY_CARD:
            return self.play_card(player.color, option.card)
        elif option.code == OptionCode.READY:
            return self.ready(player.color)
        elif option.code == OptionCode.UNDO_CARD:
            return self.undo_card(player.color)
        elif option.code == OptionCode.PASS:
            return self.drop_cards(player.color)
        else:
            raise Exception(f"Unknown option {option.code}")

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
        if all(len(player.hand) == 0 for player in self.players.values()):
            self.next_deal()
        else:
            self.current_player = self.next_player(self.current_player)
            while len(self.current_player.hand) == 0:
                self.current_player = self.next_player(self.current_player)
            self.turn()

    def next_deal(self):
        self.current_player = self.next_player(self.current_dealer)
        self.current_player.options = [Option(OptionCode.DEAL, "Delen")]
        self.current_player.message = f"Jij bent aan de beurt om te delen."
        self.current_player.set_state(StateCode.DEAL)
        
        for player in self.players.values():
            if player.color != self.current_player.color:
                player.message = f"{self.current_player.name} is aan de beurt om te delen"
                player.set_state(StateCode.DEAL_OTHER, other_player_name=self.current_player.name) 

    def turn(self):
        self.current_player.options = [Option(OptionCode.PLAY_CARD, card.denom, card=card) for card in self.current_player.hand]
        self.current_player.options.append(Option(OptionCode.PASS, "Pas"))
        self.current_player.message = "Kies een kaart om te spelen"
        self.current_player.set_state(StateCode.PLAY_CARD)

        for player in self.players.values():
            if player.color != self.current_player.color:
                player.message = f"{self.current_player.name} is aan de beurt"
                player.set_state(StateCode.PLAY_CARD_OTHER, other_player_name=self.current_player.name) 

    def partner(self, player):
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

    print([card.__dict__ for card in game.stock], end="\n\n")
