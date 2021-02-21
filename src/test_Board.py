from unittest import TestCase

from Board import Board, Mark


class TestBoard(TestCase):
    board: Board = None

    def setUp(self) -> None:
        global board
        board = Board()

    def test_newBoardShouldBeEmpty(self):
        self.assertTrue(board.isEmpty())

    def test_setValue_getValue(self):
        board.setValueAt(0, 0, Mark.CROSS)
        self.assertEqual(Mark.CROSS, board.getValueAt(0, 0))
        self.assertEqual(Mark.DEFAULT, board.getValueAt(1, 1))

    def test_winningTopRow(self):
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(0, 1, Mark.CROSS)
        board.setValueAt(0, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_winningBottomRow(self):
        board.setValueAt(2, 0, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        board.setValueAt(2, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_winningFirstColumn(self):
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(2, 0, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_winningLastColumn(self):
        board.setValueAt(0, 1, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_winningDiagonal1(self):
        board.setValueAt(0, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 2, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_winningDiagonal2(self):
        board.setValueAt(0, 2, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 0, Mark.CROSS)
        self.assertTrue(board.gameOver())
        self.assertEqual(Mark.CROSS, board.winner())

    def test_draw(self):
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
        self.assertTrue(board.isFull())
        self.assertEqual(Mark.DEFAULT, board.winner())

    def test_rowWinningCells(self):
        board.setValueAt(1, 0, Mark.CROSS)
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(1, 2, Mark.CROSS)

        winningCells = [(1, 0), (1, 1), (1, 2)]

        self.assertTrue(board.gameOver())
        self.assertListEqual(winningCells, board.getWinningCells())

    def test_columnWinningCells(self):
        board = Board()
        board.setValueAt(1, 1, Mark.CROSS)
        board.setValueAt(2, 1, Mark.CROSS)
        board.setValueAt(0, 1, Mark.CROSS)

        winningCells = [(0, 1), (1, 1), (2, 1)]

        self.assertTrue(board.gameOver())
        self.assertListEqual(winningCells, board.getWinningCells())
