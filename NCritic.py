from collections import defaultdict
from random import random
import torch
from torch import optim, nn


class NCritic:
    def __init__(self, gamma, rate, trace_decay, layer_sizes):
        self._gamma = gamma
        self._l_rate = rate
        self._trace_decay = trace_decay

        self.model = nn.Sequential()
        for i in range(1, len(layer_sizes)):
            inp = layer_sizes[i - 1]
            output = layer_sizes[i]

            layer_name = "layer%d" % i
            sig_name = "activation%d" % i
            self.model.add_module(layer_name, nn.Linear(inp, output))
            self.model.add_module(sig_name, nn.ReLU())

        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        self._eligibilitys = list()


        self.dtype = torch.float
        self.device = torch.device("cpu")

    def update_from_td_error(self, current_episode, td_error):
        for i, p in enumerate(self.model.parameters()):
            if not p.requires_grad:
                continue
            self._eligibilitys[i][:] = (self._gamma * self._trace_decay * self._eligibilitys[i]) + (
                    self._gamma * p.grad)
            p.grad[:] = td_error.squeeze() * self._eligibilitys[i]

        self.optimizer.step()

    def calculate_td_error(self, r, new_state, old_state):
        new = self._to_tensor(new_state)
        old = self._to_tensor(old_state)

        params = list(self.model.parameters())

        v_new_state = self.model(new)
        v_old_state = self.model(old)

        self.optimizer.zero_grad()
        (-v_new_state).backward()  # why negative??? not sure, someone at stackoverflow suggested it, and it works

        if len(self._eligibilitys) is 0:
            for i, p in enumerate(params):
                if not p.requires_grad:
                    continue
                self._eligibilitys.append(torch.zeros_like(p.grad, requires_grad=False))

        td_error = r + self._gamma * v_new_state.data - v_old_state.data

        return td_error

    def _to_tensor(self, board_state):
        return torch.tensor(self.encode(board_state), device=self.device, dtype=self.dtype, requires_grad=True)

    def new_episode(self):
        self._eligibilitys.clear()

    @staticmethod
    def encode(new_state):
        code = []

        for row in new_state.get_board():
            for cell in row:
                code.append(cell)
        return code
