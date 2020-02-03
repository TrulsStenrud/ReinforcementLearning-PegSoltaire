from Boards.HexBoard import HexBoard


class TriangleBoard(HexBoard):
    def __init__(self, size, free_cells):
        board = self.makeBoard(size)

        for cell in free_cells:
            board[cell[0]][cell[1]] = 0

        super().__init__(tuple(map(lambda x: tuple(x), board)))

    def makeBoard(self, size):
        board = []
        for i in range(0, size):
            board.append([])
            for j in range(0, size):
                board[i].append(1)
            size -= 1

        return board

