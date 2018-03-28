from pyMiniJass.game import Game
from pyMiniJass.player.random_player import RandomPlayer


def test_game():
    players = [RandomPlayer(name=str(i)) for i in range(4)]
    game = Game(players=players)
    game.play()
    points_team1 = sum(player.points for player in game.team1)
    points_team2 = sum(player.points for player in game.team2)
    assert points_team1 + points_team2 == 72
