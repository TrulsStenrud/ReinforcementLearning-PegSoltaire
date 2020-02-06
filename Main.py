from collections import defaultdict
from random import random

from keras import Sequential

from keras.layers import Dense
import keras

from Boards.DiamondBoard import DiamondBoard, SortOfDiamondBoard
import networkx as nx
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from Boards.DummyBoard import DummyBoard
from Boards.Triangle import TriangleBoard
from Critic import Critic
from splitgd import SplitGD


class Actor:
    def __init__(self, learning_rate, trace_decay, gamma, epsilon, epsilon_decay):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.trace_decay = trace_decay
        self.policy = defaultdict(lambda: random())
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def get_action(self, state):
        actions = state.get_actions()

        if random() < self.epsilon:
            n = int(random() * len(actions))
            return actions[n]
        else:
            return max(actions, key=lambda x: self.policy[(state, x)])

            ## trying to pick values based on probability, but im not using it
            ## now
            m = min(map(lambda x: self.policy[(state, x)], actions))
            tot = sum(map(lambda x: self.policy[(state, x)] - m, actions))

            if tot == 0:
                n = int(random() * len(actions))
                return actions[n]

            r = random()
            counter = 0
            for action in actions:
                counter += (self.policy[(state, action)] - m) / tot
                if counter > r:
                    return action

    def update_td_error(self, current_episode, td_error):
        eligibility = 1

        for sa in reversed(current_episode):
            self.policy[sa] += self.learning_rate * td_error * eligibility
            eligibility *= self.gamma * self.trace_decay

    def new_episode(self):
        self.epsilon *= self.epsilon_decay


class NCritic:
    def __init__(self, gamma, rate, trace_decay):
        self._valueFunction = defaultdict(lambda: random())
        self._gamma = gamma
        self._l_rate = rate
        self._trace_decay = trace_decay

        model = keras.Sequential()
        activation = 'sigmoid'

        model.add(Dense(3, input_shape=[3], activation=activation))
        #model.add(Dense(16, activation=activation))
        model.add(Dense(1, activation=activation))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = model

    def update_stuff(self, current_episode, td_error):
        pass

    def calculate_td_error(self, r, new_state, old_state):
        a = SplitGD(self.model)
        features = [tf.convert_to_tensor(self.encode(old_state)), tf.convert_to_tensor(self.encode(new_state))]
        targets = [[0], [0]]
        x = np.array([1, 1, 0])
        y = np.array([[0]])
        #self.model.fit(x, y)

        a.fit(x, y)

        pass

    def new_episode(self):
        pass

    @staticmethod
    def encode(new_state):
        code = []

        for row in new_state.get_board():
            for cell in row:
                code.append(cell)
        return code


def do_reinforcement_learning(actor, critic, init_state, n_episodes):
    remaining_pegs = list()
    for ep in range(0, n_episodes):
        new_state = init_state
        old_state = new_state
        current_episode = list()

        while not old_state.is_terminate_state():
            action = actor.get_action(old_state)
            current_episode.append((old_state, action))

            new_state = old_state.do_action(action)
            r = new_state.reward()

            td_error = critic.calculate_td_error(r, new_state, old_state)

            critic.update_stuff(current_episode, td_error)
            actor.update_td_error(current_episode, td_error)

            old_state = new_state

        # print(old_state.reward())
        actor.new_episode()
        critic.new_episode()
        remaining_pegs.append(old_state.peg_count())
    #  for state in current_episode:
    draw_state(old_state)
    plot(remaining_pegs)


def plot(remaining_pegs):
    plt.plot(remaining_pegs)
    plt.ylabel('Remaining pegs')
    plt.show()


def draw_state(state):
    G = nx.Graph()

    edges = state.get_edges()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    colors = list()
    board = state.get_board()
    for node in G.nodes:
        if board[node[0]][node[1]] == 0:
            colors.append('red')
        else:
            colors.append('black')
    my_pos = nx.spring_layout(G, seed=5, iterations=50)

    nx.draw(G, pos=my_pos, node_color=colors)
    plt.show()


def main():

    n_episodes = 1000
    gamma = 0.9  # discount rate γ
    learning_rate_a = 0.8  # α
    learning_rate_c = 0.8  # α
    trace_decay = 0.8
    epsilon = 0.5
    epsilon_decay = 0.9

    actor = Actor(learning_rate_a, trace_decay, gamma, epsilon, epsilon_decay)
    critic = Critic(gamma, learning_rate_c, trace_decay)
    #critic = NCritic(gamma, learning_rate_c, trace_decay)

    free_cells = list()
    free_cells.append((2, 1))

    init_state = DiamondBoard(5, free_cells)
    init_state = SortOfDiamondBoard()

    # init_state = DummyBoard()

    do_reinforcement_learning(actor, critic, init_state, n_episodes)

if __name__ == "__main__":
    main()
