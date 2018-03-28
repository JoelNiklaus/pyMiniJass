import logging
import random
from collections import namedtuple

from pyMiniJass.dealer import Dealer
from pyMiniJass.rules.stich_rules import stich_rule

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, players):
        assert len(players) == 4
        self.players = players
        self.team1 = [players[0], players[2]]
        self.team2 = [players[1], players[3]]
        self.points_team1 = 0
        self.points_team2 = 0

    def play(self):
        dealer = Dealer(players=self.players)
        dealer.shuffle_cards()
        dealer.deal_cards()

        start_player_index = random.randint(0, 3)

        for i in range(4):
            pass

    def play_stich(self, start_player_index):
        first_card = self.play_card(first_card=None, player=self.players[start_player_index])
        cards_on_table = [PlayedCard(player=self.players[start_player_index], card=first_card)]
        for i in get_player_index(start_index=start_player_index):
            current_player = self.players[i]
            card = self.play_card(first_card=first_card, player=current_player)
            cards_on_table.append(PlayedCard(player=current_player, card=card))
        stich = stich_rule(played_cards=cards_on_table)
        return stich

    def play_card(self, first_card, player):
        is_allowed_card = False
        generator = player.choose_card(state=self.get_status())
        chosen_card = next(generator)
        while not is_allowed_card:
            is_allowed_card = card_allowed(first_card=first_card, chosen_card=chosen_card, hand_cards=player.cards,
                                           trumpf=self.trumpf)
            card = generator.send(is_allowed_card)
            chosen_card = chosen_card if card is None else card
        else:
            logger.info('Table: {0}:{1}'.format(player, chosen_card))
            player.cards.remove(chosen_card)
        return chosen_card


def get_player_index(start_index):
    for i in range(1, 4):
        yield (i + start_index) % 4
