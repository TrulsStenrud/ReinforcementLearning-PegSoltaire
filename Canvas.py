import math

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget
from PyQt5.uic.properties import QtGui
import numpy as np


class Canvas(QWidget):

    def __init__(self):
        super().__init__()
        self.state = None

    def setState(self, state):
        self.state = state

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        qp = QPainter()
        qp.begin(self)

        if self.state is not None:
            self.draw_state(qp, self.state)

        qp.end()

    def draw_state(self, qp, state):
        # qp.fillRect(10, 10, 1000, 1000, Qt.SolidPattern)
        qp.setBrush(Qt.SolidPattern)
        edges = state.get_edges()
        board = state.get_board()

        for (x1, y1), (x2, y2) in edges:
            c_x1, c_y1 = self.to_coordinates(x1, y1)
            c_x2, c_y2 = self.to_coordinates(x2, y2)
            qp.drawLine(c_x1, c_y1, c_x2, c_y2)

        for x in range(0, len(board)):
            for y in range(0, len(board[x])):
                c_x, c_y = self.to_coordinates(x, y)

                qp.drawEllipse(c_x - 5, c_y - 5, 10, 10)

    def to_coordinates(self, x, y):

        offset = 100
        spacing = 50

        c_x = x * spacing + offset
        c_y = y * spacing * 0.86602540378 + offset

        c_x += (spacing / 2) * y

        return self.rotate(c_x, c_y)

    def rotate(self, px, py):
        origin = (self.width() / 2, self.height() / 2)
        ox, oy = origin

        angle = 45
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
