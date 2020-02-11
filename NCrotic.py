from collections import defaultdict
from random import random

import torch
from torch import optim, nn


class NCritic:
    def __init__(self, gamma, rate, trace_decay, layer_sizes):
        self._valueFunction = defaultdict(lambda: random())
        self._gamma = gamma
        self._l_rate = rate
        self._trace_decay = trace_decay

        self.model = nn.Sequential()
        for i in range(1, len(layer_sizes)):
            inp = layer_sizes[i - 1]
            outp = layer_sizes[i]

            layer_name = "layer%d" % i
            sig_name = "activation%d" % i
            self.model.add_module(layer_name, nn.Linear(inp, outp))
            self.model.add_module(sig_name, nn.ReLU())

        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        self.eligibilitys = list()
        self.dtype = torch.float
        self.device = torch.device("cpu")

    def update_stuff(self, current_episode, td_error):
        pass

    def calculate_td_error(self, r, new_state, old_state):
        new = torch.tensor(self.encode(new_state), device=self.device, dtype=self.dtype, requires_grad=True)
        old = torch.tensor(self.encode(old_state), device=self.device, dtype=self.dtype, requires_grad=True)
        params = list(self.model.parameters())

        self.optimizer.zero_grad()
        self.model.zero_grad()

        v_new_state = self.model(new)
        v_old_state = self.model(old)

        (-v_new_state).backward()  ## why negative??? figure out later

        if len(self.eligibilitys) is 0:
            for i, p in enumerate(params):
                if not p.requires_grad:
                    continue
                self.eligibilitys.append(torch.zeros_like(p.grad, requires_grad=False))

        delta = r + self._gamma * v_new_state.data - v_old_state.data
        self.optimizer.zero_grad()
        for i, p in enumerate(self.model.parameters()):
            if not p.requires_grad:
                continue
            self.eligibilitys[i][:] = (self._gamma * self._trace_decay * self.eligibilitys[i]) + (self._gamma * p.grad)
            p.grad[:] = delta.squeeze() * self.eligibilitys[i]

        self.optimizer.step()
        return delta

    def new_episode(self):
        self.eligibilitys.clear()
        pass

    @staticmethod
    def encode(new_state):
        code = []

        for row in new_state.get_board():
            for cell in row:
                code.append(cell)
        return code