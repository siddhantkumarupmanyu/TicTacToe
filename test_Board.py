from unittest import TestCase

from Board import Board
from Cell import Mark, Cell


class TestBoard(TestCase):

    def test_newBoardShouldBeEmpty(self):
        board = Board()
        self.assertTrue(board.isEmpty())

    def test_boardSetValue_GetValue(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        self.assertEqual(Mark.CROSS, board.getValueAt(0, 0))
        self.assertEqual(Mark.DEFAULT, board.getValueAt(1, 1))

    def test_crossWinsTheGame_TopRow(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(0, 1, Mark.CROSS)
        board.setValueAt(0, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_crossWinsTheGame_BottomRow(self):
        board = Board()
        board.setValueAt(2, 0, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        board.setValueAt(2, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_crossWinsTheGame_FirstColumn(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(2, 0, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_crossWinsTheGame_SecondColumn(self):
        board = Board()
        board.setValueAt(0, 1, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_crossWinsTheGame_Diagonal1(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_crossWinsTheGame_Diagonal2(self):
        board = Board()
        board.setValueAt(1, 2, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_gameDraw(self):
        board = Board()
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(0, 2, Mark.CIRCLE)

        board.setValueAt(0, 1, Mark.CROSS)
        board.setValueAt(1, 0, Mark.CIRCLE)

        board.setValueAt(1, 2, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CIRCLE)

        board.setValueAt(2, 0, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CIRCLE)

        board.setValueAt(2, 2, Mark.CROSS)

        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.DEFAULT, board.winner())

    def test_getWinningCells_RowCase(self):
        board = Board()
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(1, 2, Mark.CROSS)

        winningCells = [Cell(), Cell(), Cell()]
        winningCells[0].setValue(Mark.CROSS)
        winningCells[1].setValue(Mark.CROSS)
        winningCells[2].setValue(Mark.CROSS)

        self.assertTrue(board.gameOver())
        self.assertListEqual(winningCells, board.getWinningCells())

    def test_getWinningCells_ColumnCase(self):
        board = Board()
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        board.setValueAt(0, 1, Mark.CROSS)

        winningCells = [Cell(), Cell(), Cell()]
        winningCells[0].setValue(Mark.CROSS)
        winningCells[1].setValue(Mark.CROSS)
        winningCells[2].setValue(Mark.CROSS)

        self.assertTrue(board.gameOver())
        self.assertListEqual(winningCells, board.getWinningCells())
