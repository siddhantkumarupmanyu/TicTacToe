from typing import Tuple, Optional
from unittest import TestCase

from Board import Board
from Cell import Mark
from Play import Play
from Player import Player
from Renderer import Renderer


class TestPlayRenderer(Renderer):

    def __init__(self):
        self.isDraw = False
        self.winner: Optional[Player] = None
        self.drawingPlayers: Tuple[Player, Player] = tuple()
        self.lastInvalidPlayer = None
        self.lastInvalidMove = None

    def display(self, board: Board, nextMove: Player):
        super().display(board, nextMove)

    def won(self, board: Board, player: Player):
        self.winner = player

    def tie(self, board: Board, player1: Player, player2: Player):
        self.isDraw = True
        self.drawingPlayers = (player1, player2)

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        self.lastInvalidPlayer = player
        self.lastInvalidMove = move


class TestPlay(TestCase):

    def setUp(self) -> None:
        self.player1 = Player("Test Player 1", Mark.CROSS)
        self.player2 = Player("Test Player 2", Mark.CIRCLE)

        self.board = Board()

        self.testRenderer = TestPlayRenderer()

        self.play = Play(self.player1, self.player2, self.board, self.testRenderer)

    def test_InvalidMove_OutOfBoundMove(self):
        self.player1.moveEvent((3, 3))

        self.assertEqual((3, 3), self.testRenderer.lastInvalidMove)
        self.assertEqual(self.player1, self.testRenderer.lastInvalidPlayer)

        self.player1.moveEvent((0, 0))
        self.player2.moveEvent((2, 7))
        self.assertEqual((2, 7), self.testRenderer.lastInvalidMove)
        self.assertEqual(self.player2, self.testRenderer.lastInvalidPlayer)

    def test_InvalidMove_SameMove(self):
        self.player1.moveEvent((0, 0))
        self.player2.moveEvent((0, 0))

        self.assertEqual((0, 0), self.testRenderer.lastInvalidMove)
        self.assertEqual(self.player2, self.testRenderer.lastInvalidPlayer)
        self.assertEqual(Mark.CROSS, self.board.getValueAt(0, 0))

        self.player2.moveEvent((1, 1))
        self.player1.moveEvent((1, 1))
        self.assertEqual((1, 1), self.testRenderer.lastInvalidMove)
        self.assertEqual(self.player1, self.testRenderer.lastInvalidPlayer)
        self.assertEqual(Mark.CIRCLE, self.board.getValueAt(1, 1))

    def test_playDraw(self):
        self.player1.moveEvent((0, 0))
        self.player2.moveEvent((1, 1))

        self.player1.moveEvent((2, 0))
        self.player2.moveEvent((1, 0))

        self.player1.moveEvent((1, 2))
        self.player2.moveEvent((0, 1))

        self.player1.moveEvent((2, 1))
        self.player2.moveEvent((2, 2))

        self.player1.moveEvent((0, 2))

        self.assertTrue(self.testRenderer.isDraw)
        self.assertTupleEqual((self.player1, self.player2), self.testRenderer.drawingPlayers)

    def test_CircleWonGame(self):
        self.player1.moveEvent((0, 0))
        self.player2.moveEvent((1, 1))

        self.player1.moveEvent((2, 0))
        self.player2.moveEvent((1, 0))

        self.player1.moveEvent((0, 2))
        self.player2.moveEvent((1, 2))

        self.assertTupleEqual(tuple(), self.testRenderer.drawingPlayers)
        self.assertEqual(self.player2, self.testRenderer.winner)
        self.assertEqual(Mark.CIRCLE, self.testRenderer.winner.getMark())
        self.assertListEqual([(1, 0), (1, 1), (1, 2)], self.board.getWinningCells())

    def test_CrossWonGame(self):
        self.player1.moveEvent((0, 0))
        self.player2.moveEvent((1, 1))

        self.player1.moveEvent((2, 2))
        self.player2.moveEvent((2, 1))

        self.player1.moveEvent((0, 2))
        self.player2.moveEvent((1, 0))

        self.player1.moveEvent((0, 1))

        self.assertTupleEqual(tuple(), self.testRenderer.drawingPlayers)
        self.assertEqual(self.player1, self.testRenderer.winner)
        self.assertEqual(Mark.CROSS, self.testRenderer.winner.getMark())
        self.assertListEqual([(0, 0), (0, 1), (0, 2)], self.board.getWinningCells())
