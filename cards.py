import random

suits = ["hearts", "spades", "clubs", "diamonds"]
denoms = ["ace", "king", "queen", "jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

class Card(object):
    def __init__(self, suit, denom):
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

def shuffle(numberOfDecks):
    deck = [Card(x, y) for x in suits for y in denoms] + [Card(None, "joker") for _ in range(3)]
    stock = deck * numberOfDecks

    for n in range(len(stock)):
        x = random.randint(0, len(stock) - n)
        value = stock[x]
        stock[x] = stock[n]
        stock[n] = value

    return stock

if __name__ == "__main__":
    print(shuffle(2))