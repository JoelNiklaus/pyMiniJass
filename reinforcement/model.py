import os

from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import Adam
from keras.models import Sequential

def build_model(model_path, learning_rate=0.01):
    model = Sequential()
    model.add(Dense(2 * RoseInputHandler.input_size, input_shape=(RoseInputHandler.input_size,), activation='relu'))
    model.add(Dense(4 * RoseInputHandler.input_size, activation='relu'))
    model.add(Dense(2 * RoseInputHandler.input_size, activation='relu'))
    model.add(Dense(RoseInputHandler.output_size))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate))
    load_model(model, model_path)
    return model


def build_cnn_model(model_path, learning_rate=0.1):
    model = Sequential()
    model.add(Conv2D(16, (5, 5), padding='same', input_shape=(RoseInputHandler.nr_cards, 5, 1),
                     activation='relu'))
    model.add(Conv2D(32, (4, 4), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(RoseInputHandler.output_size))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate, clipnorm=1.))
    load_model(model, model_path)
    return model


def load_model(model, file_path='rl_model.h5'):
    if os.path.exists(file_path):
        model.load_weights(file_path)
        print('Load weights from existing model.')
