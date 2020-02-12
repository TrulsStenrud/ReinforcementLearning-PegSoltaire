from collections import defaultdict
from random import random


class Critic:
    def __init__(self, gamma, rate, trace_decay):
        self._valueFunction = defaultdict(lambda: 0)
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

    def update_from_td_error(self, current_episode, td_error):
        eligibility = 1
        eligibility *= self._gamma * self._trace_decay
        for sa in reversed(current_episode):
            state = sa[0]
            self._valueFunction[state] += self._l_rate * td_error * eligibility

            eligibility *= self._gamma * self._trace_decay
