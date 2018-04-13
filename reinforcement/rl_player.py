import logging
import random
from collections import deque

import numpy as np
from keras.callbacks import ReduceLROnPlateau

from pyMiniJass.game import get_team_points
from pyMiniJass.player.base_player import BasePlayer
from reinforcement.input_handler import InputHandler, index_to_card, print_state, teammate_id, opponent_ids
from reinforcement.model import build_model

logger = logging.getLogger(__name__)


class RlPlayer(BasePlayer):
    def __init__(self, name, model_path, rounds=1):
        super().__init__(name=name)
        self.input_handler = InputHandler()
        self.number_of_hand_cards = 6
        self.n_samples = 2 * rounds * 6
        self.memories = deque([], maxlen=2 * self.n_samples)
        self.model = build_model(model_path=model_path)
        self.model_t = build_model(model_path=model_path)
        self.loss = []
        self.epsilon = 0.95  # exploration rate
        self.penalty = 0.
        self.gamma = 0.95
        # self.callbacks = [ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.001)]
        self.won = 0
        self.lost = 0
        self.remis = 0
        self.current_memory = dict(used=False)
        self.previous_memory = dict(used=False)
        self.previous_points = [0, 0, 0, 0]
        self.winning = [0, 0, 0, 0]

    def remember(self, state, action, reward, next_state, done):
        self.memories.append((state, action, reward, next_state, done))

    def act(self, input_state):
        if random.uniform(0, 1) >= self.epsilon:
            random_list = [i for i in range(InputHandler.output_size)]
            random.shuffle(random_list)
            return np.random.random_sample(InputHandler.output_size), np.array(random_list)
        state = np.expand_dims(input_state, axis=0)
        act_values = self.model.predict(state)
        return act_values, np.argsort(act_values[0])[::-1]

    def replay(self):
        for turn in self.get_batch():
            states_v = np.empty((0, InputHandler.input_size))
            targets_v = np.empty((0, InputHandler.output_size))
            predictions = [self.model_t.predict(np.expand_dims(i[0], axis=0)) for i in turn]
            rewards = [i[2] for i in turn]
            actions = [i[1] for i in turn]
            states = [i[0] for i in turn]
            for i in range(len(turn)):
                target = rewards[i]
                for y in range(i + 1, len(turn)):
                    target += self.gamma * np.amax(predictions[y][0])
                target_f = predictions[i]
                target_f[0][actions[i]] = target
                states_v = np.vstack([states_v, states[i]])
                targets_v = np.vstack([targets_v, target_f])
            history = self.model.fit(states_v, targets_v, epochs=1, verbose=0)  # callbacks=self.callbacks)
            self.loss += history.history['loss']

        self.update_target()

    def update_target(self):
        weights = self.model.get_weights()
        self.model_t.set_weights(weights)

    def get_batch(self):
        n_samples = int(min(self.n_samples, len(self.memories)) / self.number_of_hand_cards)
        sample_indices = np.random.randint(n_samples, size=self.n_samples)
        samples = []
        for i in sample_indices:
            index = self.number_of_hand_cards * i
            turn = []
            for i in range(self.number_of_hand_cards):
                sample = self.memories[index + i]
                turn.append(sample)
            samples.append(turn)
        return samples

    def choose_card(self, table=None):
        self.current_memory['penalty'] = 0.
        allowed = False
        self.input_handler.update_state_choose_card(table=table, cards=self.cards, player_id=self.id)
        predictions, prediction_indexes = self.act(self.input_handler.state)
        index = 0
        while not allowed:
            card = index_to_card(prediction_indexes[index])
            allowed = yield card
            if allowed:
                self.current_memory['action'] = prediction_indexes[index]
                yield None
            else:
                index += 1
                # self.current_memory['penalty'] = -0.1
                # logger.info('not allowed card!')

    def save_state(self, done):
        if self.previous_memory['used']:
            self.remember(state=self.previous_memory['state'], action=self.previous_memory['action'],
                          reward=self.previous_memory['reward'], done=self.previous_memory['done'],
                          next_state=self.current_memory['state'])

        self.previous_memory = self.current_memory.copy()
        # print_state(self.previous_memory['state'])
        if done:
            self.previous_points = [0, 0, 0, 0]
            self.remember(state=self.previous_memory['state'], action=self.previous_memory['action'],
                          reward=self.previous_memory['reward'], done=self.previous_memory['done'],
                          next_state=None)
            self.input_handler.reset()

    def stich_over(self, stich=None):
        done = True if len(self.cards) == 0 else False
        self.current_memory['state'] = np.copy(self.input_handler.state)
        self.current_memory['reward'] = self.calculate_reward(stich['teams'], done=done) + self.current_memory[
            'penalty']
        self.current_memory['done'] = done
        self.current_memory['used'] = True
        self.save_state(done=done)
        self.input_handler.update_state_stich_over(stich, self.id)

    def calculate_reward(self, teams, done):
        points = [teams[0][0].points, teams[1][0].points, teams[0][1].points, teams[1][1].points]
        if done:
            winner = max(points)
            winner_index = points.index(winner)
            self.winning[winner_index] += 1
            return 2.0 if winner_index in [0, 2] else -2.
        gain = points[self.id] - self.previous_points[self.id] + points[teammate_id(self.id)] - self.previous_points[
            teammate_id(self.id)]
        if gain == 0:
            a, b = opponent_ids(self.id)
            gain = -(points[a] - self.previous_points[a] + points[b] - self.previous_points[b])
        self.previous_points = points[:]
        return self.normalize_points(gain)

    def reset_stats(self):
        self.winning = [0, 0, 0, 0]

    max_points_per_round = 12 + 12 + 10 + 10

    def normalize_points(self, points):
        return (points - 0) / (self.max_points_per_round - 0)
