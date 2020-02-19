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
        self.action = None
        self.spacing = 0

    def setState(self, state):
        self.state = state
        self.spacing = (self.width() - 100) / len(state.get_board())

        board = state.get_board()

        max_x = len(board) - 1

        # TODO find better way to calculate ofset and spacing/scaling
        self.spacing = 1
        maxx, maxy, minx, miny = self.calculate_bounds(board, max_x)

        self.spacing = 800.0 / max(maxx - minx, maxy - miny)

        maxx, maxy, minx, miny = self.calculate_bounds(board, max_x)
        self.offsetx = -minx + 50
        self.offsety = -miny + 50

    def calculate_bounds(self, board, max_x):
        pos = list()
        x, y = self.to_coordinates(0, 0)
        pos.append(self.rotate(x, y, 45))
        x, y = self.to_coordinates(0, len(board[0]) - 1)
        pos.append(self.rotate(x, y, 45))
        x, y = self.to_coordinates(max_x, 0)
        pos.append(self.rotate(x, y, 45))
        x, y = self.to_coordinates(max_x, len(board[max_x]) - 1)
        pos.append(self.rotate(x, y, 45))
        minx = math.inf
        maxx = -math.inf
        miny = math.inf
        maxy = -math.inf
        for x, y in pos:
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        return maxx, maxy, minx, miny

    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.localPos()
        x, y = self.to_indices(pos.x(), pos.y())
        print(x, y)
        self.state = self.state.toggle((x, y))
        self.repaint()

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        qp = QPainter()
        qp.begin(self)

        if self.state is not None:
            self.draw_state(qp, self.state)
        if self.action is not None:
            self.draw_action(qp, self.action)

        qp.end()

    def draw_state(self, qp, state):
        # qp.fillRect(10, 10, 1000, 1000, Qt.SolidPattern)
        qp.setBrush(Qt.SolidPattern)
        edges = state.get_edges()
        board = state.get_board()

        for (x1, y1), (x2, y2) in edges:
            c_x1, c_y1 = self.convert(x1, y1)
            c_x2, c_y2 = self.convert(x2, y2)

            qp.drawLine(c_x1, c_y1, c_x2, c_y2)

        for x in range(0, len(board)):
            for y in range(0, len(board[x])):
                c_x, c_y = self.convert(x, y)

                if board[x][y] == 1:
                    size = self.spacing * 0.2
                elif board[x][y] == 0:
                    size = self.spacing * 0.05

                qp.drawEllipse(c_x - size / 2, c_y - size / 2, size, size)

    def convert(self, x, y):
        c_x, c_y = self.to_coordinates(x, y)
        c_x, c_y = self.rotate(c_x, c_y, 45)
        c_x += self.offsetx
        c_y += self.offsety
        return c_x, c_y

    def to_indices(self, c_x, c_y):
        c_x -= self.offsetx
        c_y -= self.offsety
        c_x, c_y = self.rotate(c_x, c_y, -45)

        y = c_y / (self.spacing * 0.86602540378)
        c_x -= (self.spacing / 2) * y
        x = c_x / self.spacing

        return round(x), round(y)

    def to_coordinates(self, x, y):

        c_x = x * self.spacing
        c_y = y * self.spacing * 0.86602540378

        c_x += (self.spacing / 2) * y

        return c_x, c_y

    def rotate(self, px, py, angle):
        origin = (self.width() / 2, self.height() / 2)
        ox, oy = origin

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
