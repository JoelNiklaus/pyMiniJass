import os

from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import Adam
from keras.models import Sequential

from reinforcement.input_handler import InputHandler


def build_model(model_path, learning_rate=0.01):
    model = Sequential()
    model.add(Dense(2 * InputHandler.input_size, input_shape=(InputHandler.input_size,), activation='relu'))
    model.add(Dense(4 * InputHandler.input_size, activation='relu'))
    model.add(Dense(2 * InputHandler.input_size, activation='relu'))
    model.add(Dense(InputHandler.output_size))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate))
    load_model(model, model_path)
    return model


def build_cnn_model(model_path, learning_rate=0.1):
    model = Sequential()
    model.add(Conv2D(16, (5, 5), padding='same', input_shape=(InputHandler.round_offset, 4, 1), activation='relu'))
    model.add(Conv2D(32, (4, 4), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(InputHandler.output_size))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate, clipnorm=1.))
    load_model(model, model_path)
    return model


def load_model(model, file_path='rl_model.h5'):
    if os.path.exists(file_path):
        model.load_weights(file_path)
        print('Load weights from existing model.')
