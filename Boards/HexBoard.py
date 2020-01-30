class HexBoard:

    def __init__(self, board):
        self.board = board
        self.actions = []
        self.__initatePossibleActions__()

    def __eq__(self, obj):
        return isinstance(obj, HexBoard) and obj.board == self.board

    def __copy__(self):
        return HexBoard(list(map(lambda x: x.copy(), self.board)))

    def get_actions(self):
        return self.actions.copy()

    def __initatePossibleActions__(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] == 1:
                    for action in self.__getActionsFor__((i, j)):
                        self.actions.append(action)

    def __getActionsFor__(self, pos):
        north_target = (pos[0], pos[1] - 1)
        north_dest = (pos[0], pos[1] - 2)

        south_target = (pos[0], pos[1] + 1)
        south_dest = (pos[0], pos[1] + 2)

        east_target = (pos[0] + 1, pos[1])
        east_dest = (pos[0] + 2, pos[1])

        west_target = (pos[0] - 1, pos[1])
        west_dest = (pos[0] - 2, pos[1])

        north_east_target = (pos[0] + 1, pos[1] - 1)
        north_east_dest = (pos[0] + 2, pos[1] - 2)

        south_west_target = (pos[0] - 1, pos[1] + 1)
        south_west_dest = (pos[0] - 2, pos[1] + 2)

        valid_actions = list();

        self.__checkAction__(pos, north_target, north_dest, valid_actions)
        self.__checkAction__(pos, south_target, south_dest, valid_actions)
        self.__checkAction__(pos, east_target, east_dest, valid_actions)
        self.__checkAction__(pos, west_target, west_dest, valid_actions)
        self.__checkAction__(pos, north_east_target, north_east_dest, valid_actions)
        self.__checkAction__(pos, south_west_target, south_west_dest, valid_actions)

        return valid_actions

    def __checkAction__(self, pos, target, dest, return_actions):
        if self.__isAPosition__(dest) and self.__isAPosition__(target):
            if self.board[target[0]][target[1]] == 1 and self.board[dest[0]][dest[1]] == 0:
                return_actions.append((pos, target, dest))

    def do_action(self, action):
        if action not in self.actions:
            raise Exception("Impossible action")

        new_board = list(map(lambda x : x.copy(), self.board))

        pos = action[0]
        target = action[1]
        dest = action[2]

        new_board[pos[0]][pos[1]] = 0
        new_board[target[0]][target[1]] = 0
        new_board[dest[0]][dest[1]] = 1

        return HexBoard(new_board)

    def __isAPosition__(self, pos):
        x = pos[0]
        y = pos[1]

        return 0 <= x < len(self.board) and 0 <= y < len(self.board[x])
