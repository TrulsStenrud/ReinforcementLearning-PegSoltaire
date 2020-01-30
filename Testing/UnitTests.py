import unittest

from Boards.DiamondBoard import DiamondBoard


class UnitTests(unittest.TestCase):

    def test_boards_equal(self):
        actual = DiamondBoard(5)
        expected = DiamondBoard(5)
        self.assertEqual(actual, expected, "Two boards created with the same parameters should be equal")

    def test_equality_after_action(self):
        actual = DiamondBoard(5)
        expected = DiamondBoard(5)

        action1 = actual.get_actions()[4]
        action2 = expected.get_actions()[4]

        actual = actual.do_action(action1)
        expected = expected.do_action(action2)

        self.assertEqual(actual, expected, "Two squal boards doing the same action should result in equal boards")

    def test_not_equal_after_action(self):
        board = DiamondBoard(5)
        action = board.get_actions()[2]
        newBoard = board.do_action(action)

        self.assertNotEqual(board, newBoard, "Boards should not be equal after action")


if __name__ == '__main__':
    unittest.main()
