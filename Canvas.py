from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class Canvas(QWidget):

    def __init__(self):
        super().__init__()
        self.state = None
        self.stuff = None

    def set_grid(self, state):
        self.state = state

    def initiate_animation(self, stuff):
        self.stuff = stuff

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.drawEllipse(10, 10, 100, 100)


