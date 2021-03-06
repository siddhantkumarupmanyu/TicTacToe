from unittest import TestCase

from AIPlayer import AIPlayer
from Board import Board, Mark


class TestAIPlayer(TestCase):

    def test_gameOver(self):
        board = Board()
        for i in range(3):
            board.setValueAt(i, 0, Mark.CROSS)
            board.setValueAt(i, 1, Mark.CROSS)
            board.setValueAt(i, 2, Mark.CROSS)
        aiInput = AIPlayer(Mark.CIRCLE, board)

        self.assertEqual((-1, -1), aiInput.getMove())

    def test_case1(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)

        board.setValueAt(2, 0, Mark.CIRCLE)
        board.setValueAt(2, 1, Mark.CIRCLE)

        aiInput = AIPlayer(Mark.CIRCLE, board)

        self.assertEqual((2, 2), aiInput.getMove())

    def test_case2(self):
        pass
