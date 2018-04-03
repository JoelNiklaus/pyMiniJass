import numpy as np
from matplotlib import pyplot as plt

from pyMiniJass.deck import Deck

'''
|                               played cards
|    played       |    table         |   hand cards    |
|-----------------|------------------|-----------------|

3 * 16 = 48
'''


class InputHandler:
    deck = Deck()

    nr_cards = 16
    nr_player = 4
    nr_rounds = 4

    pos_table = 1 * nr_cards
    pos_hand_cards = 2 * nr_cards

    input_size = 3 * nr_cards
    output_size = nr_cards

    def __init__(self):
        self.state = None
        self.reset()

    def reset(self):
        self.state = np.zeros(self.input_size, dtype='float32')

    def update_state_choose_card(self, table, cards):
        self.set_hand(cards)
        self.set_table(table)

    def update_state_stich_over(self, stich):
        self.set_table(stich['played_cards'])

    def set_table(self, table):
        for i in range(self.nr_cards):
            if self.state[self.pos_table + i] == 1.:
                self.state[i] = 1.
        self.state[self.pos_table:self.pos_table + self.nr_cards] = 0.
        for played_card in table:
            card = played_card.card
            self.state[self.pos_table + card_to_index(card)] = 1.

    def set_hand(self, cards):
        self.state[self.pos_hand_cards:self.pos_hand_cards + self.nr_cards] = 0.
        for card in cards:
            self.state[self.pos_hand_cards + card_to_index(card)] = 1.


def card_to_index(card):
    return InputHandler.deck.cards.index(card)


def index_to_card(index):
    return InputHandler.deck.cards[index]


def print_state(input_state):
    y = np.expand_dims(input_state, 0)
    y = y.reshape(3, 16)
    plt.imshow(y, cmap='gray')
    plt.show()
