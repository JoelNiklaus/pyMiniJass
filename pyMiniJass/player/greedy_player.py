import operator

from pyMiniJass.player.base_player import BasePlayer
from pyMiniJass.suit import Suit


class GreedyPlayer(BasePlayer):
    def choose_card(self, table=None):
        a, b = self._get_max_suit()
        if a is None:
            card = b
        elif b is None:
            card = a
        elif table:
            first_suit = table[0].card.suit
            if first_suit == Suit.A:
                card = a
            else:
                card = b
        else:
            card = a if a.value > b.value else b
        return move(card)

    def _get_max_suit(self):
        a_s = []
        b_s = []
        for card in self.cards:
            if card.suit == Suit.A:
                a_s.append(card)
            else:
                b_s.append(card)
        try:
            a = max(a_s, key=operator.attrgetter('value'))
        except ValueError:
            a = None
        try:
            b = max(b_s, key=operator.attrgetter('value'))
        except ValueError:
            b = None
        return a, b


def move(card):
    allowed = False
    while not allowed:
        allowed = yield card
        if allowed:
            yield None
