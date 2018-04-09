from pyMiniJass.card import Card
from pyMiniJass.suit import Suit


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(1, 13):
            self.cards.append(Card(value=i, suit=Suit.A))
        for i in range(1, 13):
            self.cards.append(Card(value=i, suit=Suit.B))

    def __str__(self):
        return str(self.cards)
