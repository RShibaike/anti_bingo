import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import h5py
from keras import backend as K
from keras.objectives import categorical_crossentropy


class Memory:
    def __init__(self):
        self.cap = 100  # メモリのサイズ
        self.capacity = [0 for i in range(100)]  # メモリ
        self.memory_counter = 0  # メモリのどこに入れるかに使う
        self.t_memory = 0  # メモリの使用容量

    # s:26個の数のリスト　a:0or1　r:ポイント　s_:26個の数のリスト

    def store(self, s, a, r, s_):
        if self.memory_counter == self.cap:
            self.memory_counter = 0
        transition = []
        transition.append(s)
        transition.append(a)
        transition.append(r)
        transition.append(s_)
        index = self.memory_counter % self.cap
        self.capacity[index] = transition
        self.memory_counter += 1
        if self.t_memory <= self.cap-1:
            self.t_memory += 1
        else:
            self.t_memory = self.cap-1

    def sample(self):
        indices = random.choice(self.capacity)
        return indices


class Policy:

    def __init__(self):
        self.gamma = 0.9
        self.epsilon = 0.1
        self.build_net()

    def build_net(self):
        self.model = tf.keras.Sequential()
        self.model.add(layers.Dense(26, activation='relu'))
        self.model.add(layers.Dense(26, activation='relu'))
        self.model.add(layers.Dense(2))
        # self.model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
        #                    loss='mse',
        #                    metrics=['mae'])

    def choose_action(self, states):
        if random.random() >= self.epsilon:
            action = np.argmax(self.Q_values(states))
        else:
            action = random.randrange(2)
        return action

    def Q_values(self, states):
        res = self.model.predict(np.array([states]))
        return res

    def learn_act(self, state, act, reward, next_state):
        labels = [0, 0]
        labels[0] = reward + self.gamma*np.max(self.Q_values(next_state))
        labels[1] = reward + self.gamma*np.max(self.Q_values(next_state))
        labels = np.array(labels)

        print(labels)
        print(state)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
                           loss="mse",
                           metrics=['acc'])
        self.model.fit(state, labels, epochs=1, batch_size=1)

    # def delta(self, act):
    #     def loss_function(y_true, y_pred):
    #         print(categorical_crossentropy(y_true, y_pred))
    #         print(y_true)
    #         # print(y_true[1][0])
    #         print(y_pred)
    #         # print(y_pred[0][act])
    #         # y_pred.numpy()
    #         # print(K.eval(y_true))
    #         # print(y_pred[act])
    #         # print(y_pred[act].numpy())
    #         a = (y_true - y_pred[act])**2
    #         print(a)
    #         print("aaaaaaaaaaaa")
    #         print(K.mean((y_true - y_pred[act])**2))
    #         return y_true - y_pred[act]
    #     return loss_function

    def converter(self, card, turn):
        res = np.array(card)
        res = res.flatten()
        res = np.append(res, turn)

        return res

    def save(self):
        self.model.save_weights('param.h5', save_format="h5")

    def load(self):
        self.model.load_weights('param.h5')

    def summary(self):
        print(self.model.summary())
