from typing import Tuple, Optional
from unittest import TestCase

from Board import Board, Mark
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

    def displayBoardWithNextMove(self, board: Board, nextMove: Player):
        super().displayBoardWithNextMove(board, nextMove)

    def displayWinner(self, board: Board, player: Player):
        self.winner = player

    def tie(self, board: Board, player1: Player, player2: Player):
        self.isDraw = True
        self.drawingPlayers = (player1, player2)

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        self.lastInvalidPlayer = player
        self.lastInvalidMove = move


class TestPlay(TestCase):
    player1: Player
    player2: Player
    board: Board
    testRenderer: TestPlayRenderer
    play: Play

    def setUp(self) -> None:
        global player1
        global player2
        global board
        global testRenderer
        global play
        player1 = Player("Test Player 1", Mark.CROSS)
        player2 = Player("Test Player 2", Mark.CIRCLE)
        board = Board()
        testRenderer = TestPlayRenderer()
        play = Play(player1, player2, board, testRenderer)

    def test_InvalidMove_OutOfBoundMove(self):
        player1.moveEvent((3, 3))
        self.assertEqual((3, 3), testRenderer.lastInvalidMove)
        self.assertEqual(player1, testRenderer.lastInvalidPlayer)
        player1.moveEvent((0, 0))

        player2.moveEvent((2, 7))
        self.assertEqual((2, 7), testRenderer.lastInvalidMove)
        self.assertEqual(player2, testRenderer.lastInvalidPlayer)

    def test_InvalidMove_SameMove(self):
        player1.moveEvent((0, 0))
        player2.moveEvent((0, 0))
        self.assertEqual((0, 0), testRenderer.lastInvalidMove)
        self.assertEqual(player2, testRenderer.lastInvalidPlayer)
        self.assertEqual(Mark.CROSS, board.getValueAt(0, 0))

        player2.moveEvent((1, 1))
        player1.moveEvent((1, 1))
        self.assertEqual((1, 1), testRenderer.lastInvalidMove)
        self.assertEqual(player1, testRenderer.lastInvalidPlayer)
        self.assertEqual(Mark.CIRCLE, board.getValueAt(1, 1))

    def test_playDraw(self):
        player1.moveEvent((0, 0))
        player2.moveEvent((1, 1))

        player1.moveEvent((2, 0))
        player2.moveEvent((1, 0))

        player1.moveEvent((1, 2))
        player2.moveEvent((0, 1))

        player1.moveEvent((2, 1))
        player2.moveEvent((2, 2))

        player1.moveEvent((0, 2))

        self.assertTrue(testRenderer.isDraw)
        self.assertTupleEqual((player1, player2), testRenderer.drawingPlayers)

    def test_CircleWonGame(self):
        player1.moveEvent((0, 0))
        player2.moveEvent((1, 1))

        player1.moveEvent((2, 0))
        player2.moveEvent((1, 0))

        player1.moveEvent((0, 2))
        player2.moveEvent((1, 2))

        self.assertTupleEqual(tuple(), testRenderer.drawingPlayers)
        self.assertEqual(player2, testRenderer.winner)
        self.assertEqual(Mark.CIRCLE, testRenderer.winner.getMark())
        self.assertListEqual([(1, 0), (1, 1), (1, 2)], board.getWinningCells())

    def test_CrossWonGame(self):
        player1.moveEvent((0, 0))
        player2.moveEvent((1, 1))

        player1.moveEvent((2, 2))
        player2.moveEvent((2, 1))

        player1.moveEvent((0, 2))
        player2.moveEvent((1, 0))

        player1.moveEvent((0, 1))

        self.assertTupleEqual(tuple(), testRenderer.drawingPlayers)
        self.assertEqual(player1, testRenderer.winner)
        self.assertEqual(Mark.CROSS, testRenderer.winner.getMark())
        self.assertListEqual([(0, 0), (0, 1), (0, 2)], board.getWinningCells())
