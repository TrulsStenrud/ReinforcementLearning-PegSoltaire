from Boards.HexBoard import HexBoard


class DummyBoard(HexBoard):
    def __init__(self):
        board = self.makeBoard()

        board[2][0] = 1
        board[2][2] = 1
        board[2][3] = 1


        super().__init__(tuple(map(lambda x: tuple(x), board)))

    def makeBoard(self):
        board = []
        for i in range(0, 5):
            board.append([])
            for j in range(0, 5):
                board[i].append(0)

        return board

