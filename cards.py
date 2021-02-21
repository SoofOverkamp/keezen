import random

suits = ["hearts", "spades", "clubs", "diamonds"]
denoms = ["ace", "king", "queen", "jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]


class Card(object):
    def __init__(self, uid, suit, denom):
        self.uid = uid
        self.suit = suit
        self.denom = denom

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        elif isinstance(other, dict):
            return self.__dict__ == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def shuffle(number_of_decks):
    deck = [(x, y) for x in suits for y in denoms] + [(None, "joker") for _ in range(3)]
    stock = deck * number_of_decks

    stock = zip(stock, range(len(stock)))
    stock = [Card(uid, x, y) for ((x, y), uid) in stock]
    random.shuffle(stock)

    return stock

if __name__ == "__main__":
    print(shuffle(2))