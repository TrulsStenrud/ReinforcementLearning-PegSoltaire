class HexBoard:

    def __init__(self, board):
        self.__board__ = board
        self.__actions__ = self.__initatePossibleActions__()

    def __eq__(self, obj):
        return isinstance(obj, HexBoard) and obj.__board__ == self.__board__

    def __copy__(self):
        return HexBoard(list(map(lambda x: x.copy(), self.__board__)))

    def __hash__(self):
        return self.__board__.__hash__()

    def __initatePossibleActions__(self):
        actions = list()
        for i in range(0, len(self.__board__)):
            for j in range(0, len(self.__board__[i])):
                if self.__board__[i][j] == 1:
                    for action in self.__getActionsFor__((i, j)):
                        actions.append(action)

        return tuple(actions)

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
            if self.__board__[target[0]][target[1]] == 1 and self.__board__[dest[0]][dest[1]] == 0:
                return_actions.append((pos, target, dest))

    def __isAPosition__(self, pos):
        x = pos[0]
        y = pos[1]

        return 0 <= x < len(self.__board__) and 0 <= y < len(self.__board__[x])

    def __reward__(self):
        if not self.is_terminate_state():
            return 0

        reward = 100
        count = self.peg_count()

        if count == 1:
            return reward

        return -reward  # * count

    def peg_count(self):
        return sum(map(lambda x: sum(x), self.__board__))

    def is_terminate_state(self):
        return len(self.__actions__) == 0

    def do_action(self, action):
        if action not in self.__actions__:
            raise Exception("Impossible action")

        new_board = list(map(lambda x: list(x), self.__board__))

        pos_x, pos_y = action[0]
        target_x, target_y = action[1]
        dest_x, dest_y = action[2]

        new_board[pos_x][pos_y] = 0
        new_board[target_x][target_y] = 0
        new_board[dest_x][dest_y] = 1

        new_state = HexBoard(tuple(map(lambda x: tuple(x), new_board)))

        return new_state, new_state.__reward__()

    def get_board(self):
        return self.__board__

    def get_actions(self):
        return self.__actions__

    def toggle(self, pos):
        x = pos[0]
        y = pos[1]
        if not self.__isAPosition__(pos):
            return self

        new_board = list(map(lambda x: list(x), self.__board__))
        value = new_board[x][y]
        if value == 1:
            new_board[x][y] = 0
        else:
            new_board[x][y] = 1

        return HexBoard(tuple(map(lambda x: tuple(x), new_board)))

    def get_edges(self):
        edges = list()
        for x in range(0, len(self.__board__)):
            for y in range(0, len(self.__board__[x])):
                west = (x - 1, y)
                south = (x, y + 1)
                south_west = (x - 1, y + 1)

                if self.__isAPosition__(west):
                    edges.append(((x, y), west))

                if self.__isAPosition__(south):
                    edges.append(((x, y), south))

                if self.__isAPosition__(south_west):
                    edges.append(((x, y), south_west))
        return edges
