import random

from pyMiniJass.player.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def choose_card(self, state=None):
        if state:
            first_card = state[-1]['played_cards'][0].card
        else:
            first_card = None
        cards = self.allowed_cards(first_card=first_card)
        return move(choices=cards)


def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
