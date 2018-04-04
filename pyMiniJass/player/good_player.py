import operator

from pyMiniJass.player.base_player import BasePlayer
from pyMiniJass.suit import Suit


class GoodPlayer(BasePlayer):
    def choose_card(self, table=None):
        max_a, max_b = self._get_max_suit()
        if not table:
            if max_b is None:
                card = max_a
            elif max_a is None:
                card = max_b
            else:
                if max_a.value > max_b.value:
                    card = max_a
                else:
                    card = max_b
        else:
            min_a, min_b = self._get_min_suit()
            first_suit = table[0].card.suit
            first_value = table[0].card.value
            if first_suit == Suit.A:
                if max_a is not None:
                    if max_a.value > first_value:
                        card = max_a
                    else:
                        card = min_a
                else:
                    card = min_b
            else:
                if max_b is not None:
                    if max_b.value > first_value:
                        card = max_b
                    else:
                        card = min_b
                else:
                    card = min_a
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

    def _get_min_suit(self):
        a_s = []
        b_s = []
        for card in self.cards:
            if card.suit == Suit.A:
                a_s.append(card)
            else:
                b_s.append(card)
        try:
            a = min(a_s, key=operator.attrgetter('value'))
        except ValueError:
            a = None
        try:
            b = min(b_s, key=operator.attrgetter('value'))
        except ValueError:
            b = None
        return a, b


def move(card):
    allowed = False
    while not allowed:
        allowed = yield card
        if allowed:
            yield None
