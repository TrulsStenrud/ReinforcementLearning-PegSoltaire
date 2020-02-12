from collections import defaultdict
from random import random


class Actor:
    def __init__(self, learning_rate, trace_decay, gamma, epsilon, epsilon_decay):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.trace_decay = trace_decay
        self.policy = defaultdict(lambda: 0)
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
