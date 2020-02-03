from collections import defaultdict
from random import random

from Boards.DiamondBoard import DiamondBoard
import networkx as nx
import matplotlib.pyplot as plt

from Boards.DummyBoard import DummyBoard
from Boards.Triangle import TriangleBoard


class Actor:
    def __init__(self, learning_rate, trace_decay, gamma):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.trace_decay = trace_decay
        self.policy = defaultdict(lambda: random())

    def get_action(self, state, epsilon):
        actions = state.get_actions()

        if random() < epsilon:
            n = int(random() * len(actions))
            return actions[n]
        else:
            points = list(map(lambda x: self.policy[(state, x)], actions))
            action = max(actions, key=lambda x: self.policy[(state, x)])
            return action

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
                counter += (self.policy[(state, action)]-m)/tot
                if counter > r:
                    return action

    def update_td_error(self, current_episode, td_error):
        eligibility = 1

        for sa in reversed(current_episode):
            self.policy[sa] += self.learning_rate*td_error*eligibility
            eligibility *= self.gamma*self.trace_decay

    def new_episode(self):
        pass


class Critic:
    def __init__(self, gamma, rate, trace_decay):
        self._valueFunction = defaultdict(lambda: random())
        self._gamma = gamma
        self._l_rate = rate
        self._trace_decay = trace_decay

    def calculate_td_error(self, r, new_state, old_state):
        self._valueFunction[old_state] += self._l_rate * (r + self._gamma * self._valueFunction[new_state]
                                                          - self._valueFunction[old_state])

        v_new_state = self._valueFunction[new_state]
        v_old_state = self._valueFunction[old_state]
        td_error = r + self._gamma * v_new_state - v_old_state
        return td_error

    def new_episode(self):
        pass

    def update_stuff(self, current_episode, td_error):
        eligibility = 1
        eligibility *= self._gamma * self._trace_decay
        for sa in reversed(current_episode):
            state = sa[0]
            self._valueFunction[state] += self._l_rate * td_error * eligibility

            eligibility *= self._gamma * self._trace_decay


def main():
    remaining_pegs = list()
    ##remaining_pegs = list()

    n_episodes = 500
    gamma = 0.9  # discount rate γ
    learning_rate_a = 0.8  # α
    learning_rate_c = 0.8  # α
    trace_decay = 0.8
    epsilon = 0.5
    epsilon_decay = 0.5

    actor = Actor(learning_rate_a, trace_decay, gamma)
    critic = Critic(gamma, learning_rate_c, trace_decay)

    free_cells = list()
    #free_cells.append((1, 1))
    free_cells.append((2, 2))
    init_state = TriangleBoard(5, free_cells)


   # init_state = DummyBoard()

    for ep in range(0, n_episodes):
        new_state = init_state
        old_state = new_state
        current_episode = list()

        while not old_state.is_terminate_state():

            action = actor.get_action(old_state, epsilon)
            current_episode.append((old_state, action))

            new_state = old_state.do_action(action)
            r = new_state.reward()

            td_error = critic.calculate_td_error(r, new_state, old_state)

            critic.update_stuff(current_episode, td_error)
            actor.update_td_error(current_episode, td_error)

            old_state = new_state

        #print(old_state.reward())
        actor.new_episode()
        critic.new_episode()
        remaining_pegs.append(old_state.peg_count())
        epsilon *= epsilon_decay

  #  for state in current_episode:
    draw_state(old_state)
    plot(remaining_pegs)



def plot(remaining_pegs):
    plt.plot(remaining_pegs)
    plt.ylabel('Remaining pegs')
    plt.show()


#    for sa in currentEpisode:
#        draw_state(sa[0])




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
    my_pos = nx.spring_layout(G, seed=4, iterations=50)

    nx.draw(G, pos=my_pos, node_color=colors)
    plt.show()


def maint():
    print("t")



if __name__ == "__main__":
    main()
