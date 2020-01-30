from Boards.HexBoard import HexBoard


class DiamondBoard(HexBoard):
    def __init__(self, size):
        board = self.makeBoard(size)
        middlePosition = round(size/2)
        board[middlePosition][middlePosition] = 0
        super().__init__(tuple(map(lambda x: tuple(x), board)))

    def makeBoard(self, size):
        board = []
        for i in range(0, size):
            board.append([])
            for j in range(0, size):
                board[i].append(1)

        return board

