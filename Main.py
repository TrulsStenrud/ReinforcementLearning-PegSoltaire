from Boards.DiamondBoard import DiamondBoard
import networkx as nx
import matplotlib.pyplot as plt

def main():

    a = [(1, 2), (3, 2), (4, 3), (2, 2)]
    b = tuple(a)

    state = DiamondBoard(5)
    state2 = DiamondBoard(5)

    act = state.get_actions()
    state = state.do_action(act[2])
    state2 = state2.do_action(state2.get_actions()[2])

    print((state, state.get_actions()[1]) == (state2, state2.get_actions()[1]))
#    draw_state(state)



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
