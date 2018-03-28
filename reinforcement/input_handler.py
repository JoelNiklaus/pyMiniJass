import numpy as np
from matplotlib import pyplot as plt

from pyMiniJass.deck import Deck

'''
|                               played cards
|    player 0     |    player 1      |    player 2     |    player 3      |  hand cards    |
|-----------------|------------------|-----------------|------------------|----------------|
|-----------------|------------------|-----------------|------------------|----------------|
|-----------------|------------------|-----------------|------------------|----------------|
|-----------------|------------------|-----------------|------------------|----------------|

5 * 16 * 4 = 320
'''


class InputHandler:
    deck = Deck()

    nr_cards = 16
    nr_player = 4
    nr_rounds = 4

    pos_player_played_card = [0, 1 * nr_cards, 2 * nr_cards, 3 * nr_cards]
    pos_hand_cards = 4 * nr_cards
    round_offset = 5 * nr_cards

    input_size = 5 * nr_cards * 4
    output_size = nr_cards

    def __init__(self):
        self.state = None
        self.round_counter = 0
        self.reset()

    def reset(self):
        self.state = np.zeros(self.input_size, dtype='float32')

    def update_state_stich(self, stich, cards):
        offset = self.round_offset * self.round_counter
        self.set_played_cards(stich['played_cards'], offset=offset)
        self.round_counter = (self.round_counter + 1) % 4

    def update_state_choose_card(self, table, cards):
        offset = self.round_offset * self.round_counter
        self.set_hand(cards, offset=offset)
        self.set_played_cards(table, offset=offset)

    def set_played_cards(self, table, offset):
        for played_card in table:
            card = played_card.card
            player = played_card.player
            self.state[offset + self.pos_player_played_card[player.id] + card_to_index(card)] = 1.

    def set_hand(self, cards, offset):
        for card in cards:
            self.state[offset + self.pos_hand_cards + card_to_index(card)] = 1.


def get_state_image(input_state):
    return np.reshape(input_state, (4, InputHandler.round_offset))


def card_to_index(card):
    return InputHandler.deck.cards.index(card)


def index_to_card(index):
    return InputHandler.deck.cards[index]


def print_state(input_state):
    y = get_state_image(input_state)
    plt.imshow(y, cmap='gray')
    plt.show()
