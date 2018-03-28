import pytest

from pyMiniJass.deck import Card
from pyMiniJass.game import PlayedCard
from pyMiniJass.player.random_player import RandomPlayer
from pyMiniJass.rules.count_rules import count_stich
from pyMiniJass.suit import Suit


@pytest.mark.parametrize("played_cards, total", [
    ([PlayedCard(player=RandomPlayer(name='a'), card=Card(value=8, suit=Suit.A)),
      PlayedCard(player=RandomPlayer(name='b'), card=Card(value=7, suit=Suit.A))], 15),
    ([PlayedCard(player=RandomPlayer(name='a'), card=Card(value=1, suit=Suit.A)),
      PlayedCard(player=RandomPlayer(name='b'), card=Card(value=8, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='c'), card=Card(value=1, suit=Suit.B)),
      PlayedCard(player=RandomPlayer(name='d'), card=Card(value=7, suit=Suit.A))], 17),
    ([PlayedCard(player=RandomPlayer(name='d'), card=Card(value=7, suit=Suit.B))], 7),
    ([], 0),
])
def test_stich(played_cards, total):
    count = count_stich(played_cards=played_cards)
    assert count == total
