import argparse
import os

import matplotlib.pyplot as plt

from pyschieber.tournament import Tournament

from schieberjassbot.rose.rose_rl_player import RoseRlPlayer
from schieberjassbot.rose.rose_random_player import RoseRandomPlayer


def run(log_dir, episodes, rounds, save_plot):
    model_path_1 = log_dir + '/rl1_model_rose.h5'
    model_path_2 = log_dir + '/rl2_model_rose.h5'
    rl_player_1 = RoseRlPlayer(name='RL1', model_path=model_path_1, rounds=rounds)
    rl_player_2 = RoseRlPlayer(name='RL2', model_path=model_path_2, rounds=rounds)
    players = [rl_player_1, RoseRandomPlayer(name='Tick'), rl_player_2, RoseRandomPlayer(name='Track')]
    won1 = []
    won2 = []
    for e in range(episodes):
        tournament = Tournament()
        [tournament.register_player(player) for player in players]
        tournament.play(rounds=rounds)
        rl_player_1.replay()
        rl_player_2.replay()
        print_stats(rl_player_1.won, rl_player_1.lost)
        won1.append(rl_player_1.won)
        won2.append(rl_player_1.lost)
        rl_player_1.reset_stats()
    rl_player_1.model.save_weights(model_path_1)
    rl_player_2.model.save_weights(model_path_2)
    plot_stats(won1, won2, save_plot, log_dir)
    plot_loss(rl_player_1.loss, rl_player_2.loss, save_plot, log_dir)


def print_stats(won_player_1, won_player_2):
    difference = won_player_1 - won_player_2
    print('-' * 180)
    print("Difference: {0} ".format(difference))
    print("Team 1: {0}".format(won_player_1))
    print("Team 2: {0}".format(won_player_2))


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
    parser = argparse.ArgumentParser(description='SchieberJassBot', )
    parser.add_argument('-l', '--log_dir', dest='log_dir', help='Tensorboard log directory')
    parser.add_argument('-e', '--nr_episodes', dest='nr_episodes', help='Number of episodes to play', type=int)
    parser.add_argument('-r', '--rounds', dest='rounds', help='Game rounds', type=int)
    parser.add_argument('-s', '--save_plot', dest='save_plot', help='Do not save the plots', action='store_false')
    parser.set_defaults(log_dir=dir_path + '/weights', nr_episodes=10, rounds=20, save_plot=True)
    args = parser.parse_args()
    run(log_dir=args.log_dir, episodes=args.nr_episodes, rounds=args.rounds, save_plot=args.save_plot)
