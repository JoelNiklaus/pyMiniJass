from pyMiniJass.game import Game, get_team_points
from pyMiniJass.player.good_player import GoodPlayer
from pyMiniJass.player.random_player import RandomPlayer


def test_greedy_player():
    rounds = 100
    players = [GoodPlayer(name='GreedyPlayer1'), RandomPlayer(name='Tick'), GoodPlayer(name='GoodPlayer2'),
               RandomPlayer(name='Track')]
    won = 0
    lost = 0
    remis = 0
    for _ in range(rounds):
        game = Game(players=players)
        game.play()
        points_team_1 = get_team_points(game.team1)
        points_team_2 = get_team_points(game.team2)
        if points_team_1 > points_team_2:
            won += 1
        elif points_team_1 < points_team_2:
            lost += 1
        else:
            remis += 1
    print('won: ', won)
    print('lost: ', lost)
    print('remis: ', remis)
    assert won > lost
