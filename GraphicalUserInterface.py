from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSlider
from Actor import Actor
from Boards.DiamondBoard import DiamondBoard
from Boards.Triangle import TriangleBoard
from Canvas import Canvas
from Critic import Critic
from NCritic import NCritic
from RL import RL

triangle = "Triangle"
diamond = "Diamond"
table_based = "Tablebased"
neural_network = "Neural network"


class GraphicalUserInterface:
    def __init__(self):
        app = QApplication([])
        self.window = QWidget()
        layout = QGridLayout(self.window)

        self.network_canvas = Canvas()
        self.network_canvas.setMinimumSize(1000, 1000)

        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # layout.addWidget(run_btn, 0, 0)

        layout.addWidget(self.network_canvas, 0, 2, 20, 1)

        line = 0

        l = QLabel("Critic")
        self.critic = QComboBox()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.critic, line, 1)
        line += 1
        self.critic.addItem(table_based)
        self.critic.addItem(neural_network)

        l = QLabel("Layers:")
        self.layers = QLineEdit("15, 20, 1")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.layers, line, 1)
        line += 1

        l = QLabel("Shape")
        self.shape = QComboBox()
        layout.addWidget(l, line, 0)
        layout.addWidget(self.shape, line, 1)
        line += 1
        self.shape.addItem(diamond)
        self.shape.addItem(triangle)
        self.shape.currentTextChanged.connect(self.update_board)

        l = QLabel("Size:")
        self.size = QLineEdit("4")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.size, line, 1)
        self.size.textChanged.connect(self.update_board)
        line += 1

        l = QLabel("Episodes:")
        self.episodes = QLineEdit("500")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.episodes, line, 1)
        line += 1

        l = QLabel("Gamma:")
        self.gamma = QLineEdit("0.9")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.gamma, line, 1)
        line += 1

        l = QLabel("Learning rate actor:")
        self.l_actor = QLineEdit("0.8")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.l_actor, line, 1)
        line += 1

        l = QLabel("Learning rate critic:")
        self.l_critic = QLineEdit("0.8")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.l_critic, line, 1)
        line += 1

        l = QLabel("Trace decay:")
        self.trace_decay = QLineEdit("0.8")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.trace_decay, line, 1)
        line += 1

        l = QLabel("Epsilon:")
        self.epsilon = QLineEdit("0.5")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.epsilon, line, 1)
        line += 1

        l = QLabel("Epsilon decay:")
        self.epsilon_decay = QLineEdit("0.95")
        layout.addWidget(l, line, 0)
        layout.addWidget(self.epsilon_decay, line, 1)
        line += 1

        self.update_board_btn = QPushButton("Reset")
        self.update_board_btn.clicked.connect(self.update_board)
        self.update_board_btn.setMaximumWidth(100)
        layout.addWidget(self.update_board_btn, line, 0)
        line += 1

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run)
        self.run_btn.setMaximumWidth(100)
        layout.addWidget(self.run_btn, line, 0)
        line += 1

        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.setEnabled(False)

        self.winning_run = tuple()

        layout.addWidget(self.slider, line, 0, 1, 2)
        line += 1

        # window.setGeometry(400, 400, 500, 200)
        self.window.show()
        self.update_board()
        app.exec()

    def update_board(self):

        try:
            size = int(self.size.text())
        except ValueError:
            return
        if size <= 1:
            return

        cells = list()
        shape = self.shape.currentText()
        if shape == diamond:
            board = DiamondBoard(size, cells)
        elif shape == triangle:
            board = TriangleBoard(size, cells)

        self.validate_layers(sum(map(lambda x: len(x), board.get_board())))

        self.network_canvas.setState(board)
        self.network_canvas.repaint()
        self.slider.setEnabled(False)

    def validate_layers(self, input_size):
        l = self.layers.text()
        l = l.split(",")
        l = list(map(lambda x: int(x), l))

        if l[0] == input_size and l[len(l) - 1] == 1:
            return l

        l[0] = input_size
        l[len(l) - 1] = 1
        my_string = ', '.join(map(str, l))
        self.layers.setText(my_string)
        return l

    def run(self):
        init_state = self.network_canvas.state

        n_episodes = int(self.episodes.text())
        l_rate_a = float(self.l_actor.text())
        l_rate_c = float(self.l_critic.text())
        trace_decay = float(self.trace_decay.text())
        gamma = float(self.gamma.text())
        epsilon = float(self.epsilon.text())
        epsilon_decay = float(self.epsilon_decay.text())

        actor = Actor(l_rate_a, trace_decay, gamma, epsilon, epsilon_decay)

        critic_type = self.critic.currentText()

        if critic_type == table_based:
            critic = Critic(gamma, l_rate_c, trace_decay)
        elif critic_type == neural_network:
            layers = self.validate_layers(sum(map(lambda x: len(x), init_state.get_board())))
            critic = NCritic(gamma, l_rate_c, trace_decay, layers)

        self.winning_run = RL.do_actor_critic(actor, critic, init_state, n_episodes)
        if len(self.winning_run) > 0:
            self.slider.setMinimum(0)
            self.slider.setSingleStep(1)
            self.slider.setMaximum(len(self.winning_run) - 1)
            self.slider.setValue(0)
            self.slider.setEnabled(True)

    def slider_changed(self):
        if len(self.winning_run) < 1:
            return

        i = int(self.slider.value())
        self.network_canvas.setState(self.winning_run[i][0])
        self.network_canvas.repaint()
