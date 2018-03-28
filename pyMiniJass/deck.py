from collections import namedtuple

from pyMiniJass.suit import Suit

Card = namedtuple('Card', ['value', 'suit'])


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(1, 9):
            self.cards.append(Card(value=i, suit=Suit.A))
        for i in range(1, 9):
            self.cards.append(Card(value=i, suit=Suit.B))

    def __str__(self):
        return str(self.cards)
