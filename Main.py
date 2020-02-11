from collections import defaultdict
from random import random

from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout
from torch import nn
from torch import optim

import torch

from Actor import Actor
from Boards.DiamondBoard import DiamondBoard, SortOfDiamondBoard
import networkx as nx
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from Boards.DummyBoard import DummyBoard
from Boards.Triangle import TriangleBoard
from Canvas import Canvas
from Critic import Critic
from Engine import Engine
from NCrotic import NCritic
from Network import Network
from torchviz import make_dot


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


def main():
    states = Engine.reinforcement_learning()
    draw_state(states[0][0])


def test(canvas):
    canvas.update()


def playWithtorch():
    app = QApplication([])
    window = QWidget()
    layout = QGridLayout()

    runButton = QPushButton("Run")

    canvas = Canvas()
    runButton.clicked.connect(lambda: test(canvas))
    runButton.setMaximumWidth(100)
    layout.setAlignment(QtCore.Qt.AlignLeft)

    layout.addWidget(runButton, 0, 0)
    layout.addWidget(QPushButton("Woho"), 1, 0)

    layout.addWidget(canvas, 1, 1)

    window.setLayout(layout)

    window.setGeometry(400, 400, 500, 200)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
