import logging
import random
from collections import deque

import numpy as np
from keras.callbacks import ReduceLROnPlateau

from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf

logger = logging.getLogger(__name__)


class RlPlayer(BasePlayer):
    def __init__(self, name, model_path, rounds=1):
        super().__init__(name=name)
        self.input_handler = RoseInputHandler()
        self.n_samples = 20 * rounds
        self.memories = deque([], maxlen=2 * self.n_samples)
        self.model = build_cnn_model(model_path=model_path)
        self.model_t = build_cnn_model(model_path=model_path)
        self.loss = []
        self.epsilon = 0.95  # exploration rate
        self.penalty = 0.
        self.gamma = 0.95
        self.callbacks = [ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.01)]
        self.won = 0
        self.lost = 0
        self.current_memory = dict(used=False)
        self.previous_memory = dict(used=False)
        self.team_points = [0, 0]

    def remember(self, state, action, reward, next_state, done):
        self.memories.append((state, action, reward, next_state, done))

    def act(self, input_state):
        if random.uniform(0, 1) >= self.epsilon:
            random_list = [i for i in range(RoseInputHandler.output_size)]
            random.shuffle(random_list)
            return np.random.random_sample(RoseInputHandler.output_size), np.array(random_list)
        state = input_state.reshape((36, 5, 1))
        # state = np.expand_dims(input_state, axis=0)
        state = np.expand_dims(state, axis=0)
        act_values = self.model.predict(state)
        return act_values, np.argsort(act_values[0])[::-1]

    def replay(self):
        states = np.empty((0, RoseInputHandler.input_size))
        targets = np.empty((0, RoseInputHandler.output_size))
        for state, action, reward, next_state, done in self.get_batch():
            state = np.expand_dims(state, axis=0)
            next_state = np.expand_dims(next_state, axis=0)
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model_t.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            # states = np.vstack([states, state])
            # targets = np.vstack([targets, target_f])
            history = self.model.fit(state, target_f, epochs=1, verbose=0, callbacks=self.callbacks)
            self.loss += history.history['loss']
        self.update_target()

    def update_target(self):
        weights = self.model.get_weights()
        self.model_t.set_weights(weights)

    def get_batch(self):
        n_samples = min(self.n_samples, len(self.memories))
        samples = random.sample(self.memories, n_samples)
        return samples

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf = Trumpf.ROSE
            allowed = yield trumpf
            if allowed:
                yield None

    def choose_card(self, state=None):
        allowed = False
        self.input_handler.update_state_choose_card(game_state=state, cards=self.cards, player_id=self.id)
        # predictions, prediction_indexes = self.act(self.input_handler.state)
        predictions, prediction_indexes = self.act(self.input_handler.state)
        card = self.max_of_allowed_cards(state=state, predictions=predictions)
        self.current_memory['action'] = prediction_indexes[0]
        while not allowed:
            # card = index_to_card(prediction_indexes[index])
            allowed = yield card
            self.current_memory['penalty'] = 0. if card == index_to_card(prediction_indexes[0]) else -0.1
            if allowed:
                yield None
            else:
                logger.info('not allowed card!')

    def save_state(self, done):
        if self.previous_memory['used']:
            self.remember(state=self.previous_memory['state'], action=self.previous_memory['action'],
                          reward=self.previous_memory['reward'], done=self.previous_memory['done'],
                          next_state=self.current_memory['state'])

        self.previous_memory = self.current_memory.copy()
        if done:
            # print_state(self.previous_memory['state'], 0)
            self.remember(state=self.previous_memory['state'], action=self.previous_memory['action'],
                          reward=self.previous_memory['reward'], done=self.previous_memory['done'],
                          next_state=None)

    def stich_over(self, state=None):
        done = True if len(self.cards) == 0 else False
        # self.current_memory['state'] = np.copy(self.input_handler.state)
        game_state = get_state_image(self.input_handler.state).reshape((36, 5, 1))
        self.current_memory['state'] = np.copy(game_state)
        self.current_memory['reward'] = self.calculate_reward(state['teams'], done=done) + self.current_memory[
            'penalty']
        self.current_memory['done'] = done
        self.current_memory['used'] = True
        self.save_state(done=done)
        self.input_handler.update_state_stich(game_state=state, cards=self.cards, player_id=self.id)

    def calculate_reward(self, teams, done):
        if not done:
            return 0.
        team1 = teams[0]['points'] - self.team_points[0]
        team2 = teams[1]['points'] - self.team_points[1]
        self.team_points[0] = teams[0]['points']
        self.team_points[1] = teams[1]['points']
        if team1 > team2:
            self.won += 1
            return 1.
        else:
            self.lost += 1
            return -1.

    def reset_stats(self):
        self.won = 0
        self.lost = 0
        self.remis = 0

    def max_of_allowed_cards(self, predictions, state):
        allowed_cards = self.allowed_cards(state=state)
        return max_of_allowed_cards(predictions=predictions, allowed_cards=allowed_cards)


def max_of_allowed_cards(predictions, allowed_cards):
    indices_of_allowed_cards = [card_to_index(allowed_card) for allowed_card in allowed_cards]
    indices_sorted = np.argsort(predictions)[::-1]
    for i in np.nditer(indices_sorted, order='C'):
        try:
            indices_of_allowed_cards.index(i)
            return index_to_card(i)
        except ValueError:
            pass
