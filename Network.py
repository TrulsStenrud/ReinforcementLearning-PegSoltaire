from torch import nn


class Network(nn.Module):

    def __init__(self, layer_sizes):
        super().__init__()

        a = list()
        for i in range(1, len(layer_sizes)):
            a.append(
                (nn.Linear(layer_sizes[i - 1], layer_sizes[i])
                 , nn.Sigmoid())
            )
        self.layers = a

    def forward(self, x):
        for layer, thing in self.layers:
            x = layer(x)
            x = thing(x)

        return x
