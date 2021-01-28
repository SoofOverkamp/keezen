import random
from typing import List, Dict

from color import Color
from cards import Card, shuffle
from option import OptionCode, Option
from player import Player, StateCode, ErrorCode

all_colors = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

class Game(object):
    """description of class"""

    players: List[Player]
    current_player: Player
    current_dealer: Player
    stock: List[str]
    number_of_cards: int

    def __init__(self):
        self.stock = []
        self.number_of_cards = 0
        self.players = []
        self.current_player = None
        self.current_dealer = None

    def join_player(self, name):
        player = Player(name=name)
        self.players.append(player)
        player.state = StateCode.PICK_COLOR
        self.set_pick_color_state()
        return player

    def unjoin_player(self, player):
        if player.color is None:
            self.players.remove(player)
        else:
            player.name = None

        self.set_pick_color_state()

    def pick_color(self, player, color):
        color_player = next((p for p in self.players if p.color == color), None)
        if color_player is not None:
            if color_player.name is None:
                # reconnect, merge
                player.merge_from(color_player)
                self.players.remove(color_player)
            else:
                # error
                player.message = f"Kleur {color} is al gekozen door een andere speler. " + player.message
                player.set_error(ErrorCode.COLOR_ALREADY_CHOSEN, color=color) 
                return

        player.color = color
        self.set_pick_color_state()


    def set_pick_color_state(self):
        used_colors = [player.color for player in self.players if player.color is not None and player.name is not None]
        available_colors = [color for color in all_colors if color not in used_colors]

        for player in self.players:
            if player.state == StateCode.PICK_COLOR:
                player.options = [Option(OptionCode.PICK_COLOR, str(color), color=color) for color in available_colors]
                if len(used_colors) == 4 and player.color is not None:
                    player.options.append(Option(OptionCode.DEAL, "Delen"))

                if player.color is None:
                    player.message = "Kies een kleur om mee te spelen"
                else:
                    player.message = "Wie begint er met delen?"

            player.set_others(self.players)


    def deal(self, dealer):
        self.current_player = dealer
        self.current_dealer = dealer

        if self.number_of_cards <= 2:
            self.stock = shuffle(2)
            self.number_of_cards = 6
        else:
            self.number_of_cards -= 1

        for player in self.players:
            if player.color is not None:
                player.hand = self.stock[:self.number_of_cards]
                self.stock = self.stock[self.number_of_cards:]
                player.options = [Option(OptionCode.SWAP_CARD, card.denom, card=card) for card in player.hand]
                player.message = "Kies een kaart om te wisselen"
                player.state = StateCode.SWAP_CARD
                player.swap_card = None
                player.card_is_swapped = False
                player.passed = False
                player.set_current(dealer)


    def swap_card(self, player, card):
        if player.swap_card is not None:
            player.hand.append(player.swap_card)
            player.swap_card = None
        
        player.hand.remove(card)
        partner = self.partner(player)

        if partner.swap_card is None:
            player.swap_card = card
            player.message = "Wacht op je maat"
            player.state = StateCode.SWAP_CARD
            player.options = [Option(OptionCode.SWAP_CARD, card.denom, card=card) for card in player.hand]
            player.options.append(Option(OptionCode.UNDO_CARD, "Terug"))
            return

        player.hand.append(partner.swap_card)
        partner.swap_card = None
        partner.hand.append(card)
        player.card_is_swapped = True
        partner.card_is_swapped = True
        partner.options.clear()
        player.options.clear()
        player.message = ""

        if all(player.card_is_swapped for player in self.players if player.color is not None):
            self.next_turn()
        else:
            player.message = "Wacht op het andere team"
            player.state = StateCode.SWAP_CARD_OTHERS
            partner.message = "wacht op het andere team"
            partner.state = StateCode.SWAP_CARD_OTHERS


    def play_card(self, player, card):
        if player.play_card is not None:
            player.hand.append(player.play_card)
            player.play_card = None
        
        player.hand.remove(card)
        player.play_card = card
        player.options = [Option(OptionCode.UNDO_CARD, "Terug"), Option(OptionCode.READY, "Klaar")]
        player.options.extend(Option(OptionCode.PLAY_CARD, card.denom, card=card) for card in self.current_player.hand)
        player.message = f"Je speelt {card.denom}"
        player.state = StateCode.PLAY_CARD

        for other in self.players:
            if other.color != player.color:
                other.message = f"{player.name} speelt een {card.denom}"
                other.state = StateCode.PLAY_CARD_OTHER
                other.play_card = card


    def drop_cards(self, player):
        player.hand = []
        player.options = []
        player.passed = True
        player.play_card = None
        self.next_turn()


    def ready(self, player):
        player.options.clear()
        player.play_card = None
        self.next_turn()


    def undo_card(self, player):
        if player.swap_card is not None:
            player.hand.append(player.swap_card)
            player.swap_card = None
            player.options = [Option(OptionCode.SWAP_CARD, card.denom, card=card) for card in player.hand]
            player.message = "Kies een kaart om te wisselen"
            player.state = StateCode.SWAP_CARD
        else:
            player.hand.append(player.play_card)
            player.play_card = None
            self.turn()


    def play_option(self, player, option):
        if option.code == OptionCode.PICK_COLOR:
            return self.pick_color(player, option.color)
        elif option.code == OptionCode.DEAL:
            return self.deal(player)
        elif option.code == OptionCode.SWAP_CARD:
            return self.swap_card(player, option.card)
        elif option.code == OptionCode.PLAY_CARD:
            return self.play_card(player, option.card)
        elif option.code == OptionCode.READY:
            return self.ready(player)
        elif option.code == OptionCode.UNDO_CARD:
            return self.undo_card(player)
        elif option.code == OptionCode.PASS:
            return self.drop_cards(player)
        else:
            raise Exception(f"Unknown option {option.code}")

    def next_player(self, player):
        if player.color == Color.RED:
            color = Color.BLUE
        elif player.color == Color.BLUE:
            color = Color.YELLOW
        elif player.color == Color.YELLOW:
            color = Color.GREEN
        elif player.color == Color.GREEN:
            color =  Color.RED
        else:
            raise Exception(f"Unknown color {player.Color}")

        return next(player for player in self.players if player.color == color)

    def next_turn(self):
        if all(len(player.hand) == 0 for player in self.players):
            self.next_deal()
        else:
            self.current_player = self.next_player(self.current_player)
            self.current_player.play_card = None
            while len(self.current_player.hand) == 0:
                self.current_player = self.next_player(self.current_player)
            self.turn()

    def next_deal(self):
        dealer = self.next_player(self.current_dealer)
        self.current_player = dealer
        dealer.options = [Option(OptionCode.DEAL, "Delen")]
        dealer.message = f"Jij bent aan de beurt om te delen."
        dealer.state = StateCode.DEAL
        
        for player in self.players:
            player.set_current(dealer)
            if player.color != dealer.color:
                player.message = f"{dealer.name} is aan de beurt om te delen"
                player.state= StateCode.DEAL_OTHER 


    def turn(self):
        player = self.current_player
        player.options = [Option(OptionCode.PLAY_CARD, card.denom, card=card) for card in player.hand]
        player.options.append(Option(OptionCode.PASS, "Pas"))
        player.message = "Kies een kaart om te spelen"
        player.state = StateCode.PLAY_CARD
        player.play_card = None

        for player in self.players:
            player.set_current(self.current_player)
            if player.color != self.current_player.color:
                player.message = f"{self.current_player.name} is aan de beurt"
                player.state = StateCode.PLAY_CARD_OTHER 


    def partner(self, player):
        if player.color == Color.RED:
            color = Color.YELLOW
        elif player.color == Color.BLUE:
            color = Color.GREEN
        elif player.color == Color.YELLOW:
            color = Color.RED
        elif player.color == Color.GREEN:
            color = Color.BLUE
        else:
            raise Exception(f"Unknown color {player.Color}")

        return next(player for player in self.players if player.color == color)


if __name__ == "__main__":
    game = Game()
    red = game.join_player("Rood")
    blue = game.join_player("Blauw")
    yellow = game.join_player("Geel")
    green = game.join_player("Groen")
    olive = game.join_player("Olijf")
    players = [blue, yellow, green, red]
    game.pick_color(red, Color.RED)
    game.pick_color(blue, Color.BLUE)
    game.pick_color(yellow, Color.YELLOW)
    game.pick_color(green, Color.GREEN)

    for round in range(2):
        for deal in [6, 5, 4, 3, 2]:
            player = players[0]
            print(f"{player.name} deals {deal} cards")
            game.deal(player)

            for player in game.players:
                print(player.get_json(), end="\n\n")

            game.swap_card(yellow, yellow.hand[deal - 1])
            game.swap_card(red, red.hand[1])
            if round == 0:
                game.swap_card(green, green.hand[0])
            else:
                game.swap_card(olive, olive.hand[0])
            game.swap_card(blue, blue.hand[-1])

            players = players[1:] + players[:1]

            for turn in range(deal):
                for player in players:
                    card = player.hand[0]
                    game.play_card(player, card)
                    print(f"{player.name} plays {card.denom} of {card.suit}")
                    game.ready(player)

        if round == 0:
            print(green.get_json(), end="\n\n")
            green.name = None
            game.pick_color(olive, Color.GREEN)
            players = [yellow, olive, red, blue]
