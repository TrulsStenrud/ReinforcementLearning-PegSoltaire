from Boards.DiamondBoard import DiamondBoard
import networkx as nx
import matplotlib.pyplot as plt

def main():


    state = DiamondBoard(5)
    state2 = DiamondBoard(5)

    a = dict()
    a[state] = 3

    print(a[state2])



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
    my_pos = nx.spring_layout(G, seed=3, iterations=50)
    nx.draw(G, pos=my_pos, node_color=colors)
    plt.show()


if __name__ == "__main__":
    main()
