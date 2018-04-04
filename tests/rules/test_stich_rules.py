import pytest

from pyMiniJass.card import Card
from pyMiniJass.game import PlayedCard
from pyMiniJass.player.random_player import RandomPlayer
from pyMiniJass.suit import Suit
from pyMiniJass.rules.stich_rules import stich_rule


@pytest.mark.parametrize("played_cards, winner", [
    ([PlayedCard(player=RandomPlayer(name='a'), card=Card(value=8, suit=Suit.A)),
      PlayedCard(player=RandomPlayer(name='b'), card=Card(value=7, suit=Suit.A))], 'a'),
    ([PlayedCard(player=RandomPlayer(name='a'), card=Card(value=1, suit=Suit.A)),
      PlayedCard(player=RandomPlayer(name='b'), card=Card(value=8, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='c'), card=Card(value=1, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='d'), card=Card(value=7, suit=Suit.A))], 'd'),
    ([PlayedCard(player=RandomPlayer(name='a'), card=Card(value=1, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='b'), card=Card(value=8, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='c'), card=Card(value=1, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='d'), card=Card(value=7, suit=Suit.B))], 'b')
])
def test_stich(played_cards, winner):
    stich = stich_rule(played_cards=played_cards)
    assert stich.player.name == winner
