import os
import os.path

from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import Adam, SGD, RMSprop
from keras.models import Sequential
from keras.models import load_model

from reinforcement.input_handler import InputHandler

'''
def build_model(model_path, learning_rate=0.01):
    model = Sequential()
    model.add(Dense(InputHandler.input_size * 3, input_shape=(InputHandler.input_size,), activation='relu'))
    model.add(Dense(InputHandler.input_size * 9, activation='relu'))
    model.add(Dense(InputHandler.input_size * 7, activation='relu'))
    model.add(Dense(InputHandler.input_size * 3, activation='relu'))
    model.add(Dense(InputHandler.output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate, clipnorm=1.))
    load_model(model, model_path)
    return model
'''


def build_model(model_path, learning_rate=0.01):
    if os.path.exists(model_path):
        model = load_model('my_model.h5')
        print('Load existing model.')
    else:

        model = Sequential()
        model.add(Dense(InputHandler.input_size * 6, input_shape=(InputHandler.input_size,), activation='relu'))
        model.add(Dense(InputHandler.input_size * 7, activation='relu'))
        model.add(Dense(InputHandler.input_size * 3, activation='relu'))
        model.add(Dense(InputHandler.output_size, activation='linear'))
        model.compile(loss='mse', optimizer=RMSprop(lr=learning_rate, clipvalue=1.0))
    return model
