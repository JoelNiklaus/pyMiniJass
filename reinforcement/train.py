import argparse
import os

import matplotlib.pyplot as plt

from pyMiniJass.game import Game
#from pyMiniJass.player.random_player import RandomPlayer
from pyMiniJass.player.good_player import GoodPlayer
from reinforcement.rl_player import RlPlayer


def run(log_dir, episodes, rounds, no_replay):
    model_path_1 = log_dir + '/rl1_model_mini.h5'
    rl_player_1 = RlPlayer(name='RL1', model_path=model_path_1, rounds=rounds)
    players = [rl_player_1, GoodPlayer(name='Tick'), GoodPlayer(name='track'), GoodPlayer(name='Track')]

    won1 = []
    won2 = []
    for e in range(episodes):
        for _ in range(rounds):
            game = Game(players=players)
            game.play()
        rl_player_1.replay()
        print_stats_winning(winning=rl_player_1.winning)
        won1.append(rl_player_1.won)
        won2.append(rl_player_1.lost)
        if not no_replay:
            rl_player_1.reset_stats()
    rl_player_1.model.save_weights(model_path_1)


def print_stats(won_player_1, won_player_2):
    difference = won_player_1 - won_player_2
    print('-' * 180)
    print("Difference: {0} ".format(difference))
    print("Team 1: {0}".format(won_player_1))
    print("Team 2: {0}".format(won_player_2))


def print_stats_winning(winning):
    print('-' * 180)
    for i, win in enumerate(winning):
        print("Player {0}: {1} ".format(i, win))


def plot_loss(loss1, loss2, save_plot, log_dir):
    plt.figure()
    epochs = range(1, len(loss1) + 1)
    plt.plot(epochs, loss1)
    plt.plot(epochs, loss2)
    plt.legend(['Player 1 Loss', 'Player 1 Loss'], loc='upper left')
    if save_plot:
        plt.savefig(log_dir + '/loss.png')
    else:
        plt.show()


def plot_stats(won1, won2, save_plot, log_dir):
    plt.figure()
    epochs = range(1, len(won1) + 1)
    plt.plot(epochs, won1)
    plt.plot(epochs, won2)
    plt.legend(['Team 1', 'Team 2', 'Remis'], loc='upper left')
    if save_plot:
        plt.savefig(log_dir + '/team_won.png')
    else:
        plt.show()


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='pyMiniJassBot', )
    parser.add_argument('-l', '--log_dir', dest='log_dir', help='Tensorboard log directory')
    parser.add_argument('-e', '--nr_episodes', dest='nr_episodes', help='Number of episodes to play', type=int)
    parser.add_argument('-r', '--rounds', dest='rounds', help='Game rounds', type=int)
    parser.add_argument('-n', '--no-replay', dest='no_replay', help='Train RL player', action='store_true')
    parser.add_argument('-s', '--save_plot', dest='save_plot', help='Do not save the plots', action='store_false')
    parser.set_defaults(log_dir=dir_path + '/weights', nr_episodes=10, rounds=20, save_plot=True, no_replay=False)
    args = parser.parse_args()
    run(log_dir=args.log_dir, episodes=args.nr_episodes, rounds=args.rounds, no_replay=args.no_replay)
