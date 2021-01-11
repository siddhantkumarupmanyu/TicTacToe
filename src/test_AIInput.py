from unittest import TestCase

from src.AIInput import AIInput
from src.Board import Board
from src.Cell import Mark


class TestAIInput(TestCase):

    def test_case1(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)

        board.setValueAt(2, 0, Mark.CIRCLE)
        board.setValueAt(2, 1, Mark.CIRCLE)

        aiInput = AIInput(Mark.CIRCLE, board)

        self.assertEqual((2, 2), aiInput.getMove())

    def test_case2(self):
        pass
