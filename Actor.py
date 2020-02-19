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
            #return max(actions, key=lambda x: self.policy[(state, x)])

            max_value = max(map(lambda x: self.policy[(state, x)], actions))
            best_actions = list(filter(lambda x: self.policy[(state, x)] == max_value, actions))
            n = int(random() * len(best_actions))
            return best_actions[n]

    def update_td_error(self, current_episode, td_error):
        eligibility = 1

        for sa in reversed(current_episode):
            self.policy[sa] += self.learning_rate * td_error * eligibility
            eligibility *= self.gamma * self.trace_decay

    def new_episode(self):
        self.epsilon *= self.epsilon_decay
