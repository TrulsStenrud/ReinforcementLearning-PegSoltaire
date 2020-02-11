from collections import defaultdict
from random import random

from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout, \
    QLineEdit, QComboBox
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
    my_pos = nx.spring_layout(G, iterations=50)

    nx.draw(G, pos=my_pos, node_color=colors)
    plt.show()


def main():
    states = Engine.reinforcement_learning()
    draw_state(states[0][0])


class GraphicalUserInterface:
    def __init__(self):
        app = QApplication([])
        self.window = QWidget()
        layout = QGridLayout(self.window)

        self.network_canvas = Canvas()
        self.network_canvas.setMinimumSize(400, 400)

        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # layout.addWidget(run_btn, 0, 0)

        layout.addWidget(self.network_canvas, 0, 2, 20, 1)

        line = 0

        l = QLabel("Critic")
        self.critic = QComboBox()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.critic, line, 1)
        line += 1
        self.critic.addItem("Table based")
        self.critic.addItem("Neural network")

        l = QLabel("Shape")
        self.shape = QComboBox()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.shape, line, 1)
        line += 1
        self.shape.addItem("Diamond")
        self.shape.addItem("Triangle")

        l = QLabel("Size:")
        self.size = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.size, line, 1)
        line += 1

        l = QLabel("Episodes:")
        self.episodes = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.episodes, line, 1)
        line += 1

        l = QLabel("Gamma:")
        self.gamma = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.gamma, line, 1)
        line += 1

        l = QLabel("Alpha:")
        self.alpha = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.alpha, line, 1)
        line += 1

        l = QLabel("Learning rate actor:")
        self.l_actor = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.l_actor, line, 1)
        line += 1

        l = QLabel("Learning rate critic:")
        self.l_critic = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.l_critic, line, 1)
        line += 1

        l = QLabel("Trace decay:")
        self.trace_decay = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.trace_decay, line, 1)
        line += 1

        l = QLabel("Epsilon:")
        self.epsilon = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.epsilon, line, 1)
        line += 1

        l = QLabel("Epsilon decay:")
        self.epsilon_decay = QLineEdit()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.epsilon_decay, line, 1)
        line += 1

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run)
        self.run_btn.setMaximumWidth(100)
        layout.addWidget(self.run_btn, line, 0)

        # window.setGeometry(400, 400, 500, 200)
        self.window.show()

        app.exec()

    def run(self):
        cells = list()
        cells.append((1, 2))
        self.network_canvas.setState(DiamondBoard(5, cells))
        self.window.repaint()

def testing():
    a = GraphicalUserInterface()


if __name__ == "__main__":
    testing()
