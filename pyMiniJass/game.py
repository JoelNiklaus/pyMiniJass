import logging
import random
from collections import namedtuple

from pyMiniJass.dealer import Dealer
from pyMiniJass.rules.stich_rules import stich_rule, card_allowed
from pyMiniJass.rules.count_rules import count_stich
from pyMiniJass.card import card_string

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, players):
        assert len(players) == 4
        self.stiche = []
        self.players = players
        self.team1 = [players[0], players[2]]
        self.team2 = [players[1], players[3]]
        self.table = []
        self.set_player_ids()

    def set_player_ids(self):
        for i in range(len(self.players)):
            self.players[i].id = i

    def play(self):
        self.reset_players()
        dealer = Dealer(players=self.players)
        dealer.shuffle_cards()
        dealer.deal_cards()

        start_player_index = random.randint(0, 3)
        for i in range(6):
            logger.info('\nStich: {0} {1}\n'.format(i, '-' * 180))
            self.table = []
            stich = self.play_stich(start_player_index)
            self.stich_over(stich)
            self.stiche.append(stich)
            start_player_index = self.players.index(stich['stich'].player)
            logger.info('\nStich:\n\n{0}'.format(card_string([stich['stich']])))
        points = []
        for player in self.players:
            points.append(player.points)
            logger.info('Points {0}: {1}'.format(player.name, player.points))
        won_player_index = points.index(max(points))
        logger.info('\nPlayer {0} won!'.format(self.players[won_player_index].name))

    def play_stich(self, start_player_index):
        first_card = self.play_card(first_card=None, player=self.players[start_player_index])
        cards_on_table = [PlayedCard(player=self.players[start_player_index], card=first_card)]
        for i in get_player_index(start_index=start_player_index):
            current_player = self.players[i]
            card = self.play_card(first_card=first_card, player=current_player)
            cards_on_table.append(PlayedCard(player=current_player, card=card))
        played_card_stich = stich_rule(played_cards=cards_on_table)
        played_card_stich.player.points += count_stich(played_cards=cards_on_table)
        stich = dict(stich=played_card_stich, played_cards=cards_on_table, teams=[self.team1, self.team2])
        return stich

    def play_card(self, first_card, player):
        is_allowed_card = False
        generator = player.choose_card(table=self.table)
        chosen_card = next(generator)
        while not is_allowed_card:
            is_allowed_card = card_allowed(first_card=first_card, chosen_card=chosen_card, hand_cards=player.cards)
            card = generator.send(is_allowed_card)
            chosen_card = chosen_card if card is None else card
        else:
            player.cards.remove(chosen_card)
        self.table.append(PlayedCard(player=player, card=chosen_card))
        logger.info('\nTable:\n\n{0}'.format(card_string(self.table)))
        return chosen_card

    def stich_over(self, stich):
        for player in self.players:
            player.round_over(round=stich)

    def get_points_team1(self):
        return get_team_points(self.team1)

    def get_points_team2(self):
        return get_team_points(self.team2)

    def reset_players(self):
        for player in self.players:
            player.points = 0


def get_team_points(team):
    return sum(player.points for player in team)


def get_player_index(start_index):
    for i in range(1, 4):
        yield (i + start_index) % 4
