import networkx as nx
import matplotlib.pyplot as plt
from GraphicalUserInterface import GraphicalUserInterface
from RL import RL


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
    my_pos = nx.spring_layout(G, iterations=50)

    nx.draw(G, pos=my_pos, node_color=colors)
    plt.show()


def main():
    states = RL.reinforcement_learning()
    draw_state(states[0][0])


def testing():
    a = GraphicalUserInterface()


if __name__ == "__main__":
    testing()
