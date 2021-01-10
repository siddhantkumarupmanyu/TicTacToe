from typing import Tuple, List, Optional
from unittest import TestCase

from Board import Board
from Cell import Mark
from Play import Play
from Player import Player, PlayerInputInterface
from Renderer import Renderer


class TestPlayRenderer(Renderer):

    def __init__(self):
        self.isDraw = False
        self.winner: Optional[Player] = None
        self.drawingPlayers: Tuple[Player, Player] = tuple()

    def display(self, board: Board, nextMove: Player):
        super().display(board, nextMove)

    def won(self, board: Board, player: Player):
        self.winner = player

    def draw(self, board: Board, player1: Player, player2: Player):
        self.isDraw = True
        self.drawingPlayers = (player1, player2)


class TestPlayPlayerInput(PlayerInputInterface):

    def __init__(self):
        self._move: List[Tuple[int, int]] = list()
        self._i: int = -1

    def setMove(self, x: int, y: int):
        self._move.append((x, y))

    def setMoveTuple(self, xy: Tuple[int, int]):
        self._move.append(xy)

    def getMove(self) -> Tuple[int, int]:
        self._i += 1
        return self._move[self._i]


class TestPlay(TestCase):

    def setUp(self) -> None:
        self.testInput1 = TestPlayPlayerInput()
        self.testInput2 = TestPlayPlayerInput()
        self.player1 = Player(Mark.CROSS, self.testInput1)
        self.player2 = Player(Mark.CIRCLE, self.testInput2)

        self.board = Board()

        self.testRenderer = TestPlayRenderer()

        self.play = Play(self.player1, self.player2, self.board, self.testRenderer)

    def test_playDraw(self):
        self.testInput1.setMove(0, 0)
        self.testInput2.setMove(1, 1)

        self.testInput1.setMove(2, 0)
        self.testInput2.setMove(1, 0)

        self.testInput1.setMove(1, 2)
        self.testInput2.setMove(0, 1)

        self.testInput1.setMove(2, 1)
        self.testInput2.setMove(2, 2)

        self.testInput1.setMove(0, 2)

        self.play.start()

        self.assertTrue(self.testRenderer.isDraw)
        self.assertTupleEqual((self.player1, self.player2), self.testRenderer.drawingPlayers)

    def test_InvalidValue(self):
        self.testInput1.setMove(0, 0)
        self.testInput2.setMove(0, 0)
        self.testInput2.setMove(1, 1)

        self.testInput1.setMove(2, 0)
        self.testInput2.setMove(1, 0)

        self.testInput1.setMove(1, 0)
        self.testInput1.setMove(1, 2)
        self.testInput2.setMove(0, 1)

        self.testInput1.setMove(2, 1)
        self.testInput2.setMove(2, 2)

        self.testInput1.setMove(0, 2)

        self.play.start()

        self.assertEqual(Mark.CROSS, self.board.getValueAt(0, 0))
        self.assertEqual(Mark.CIRCLE, self.board.getValueAt(1, 0))

    def test_CircleWonGame(self):
        self.testInput1.setMove(0, 0)
        self.testInput2.setMove(1, 1)

        self.testInput1.setMove(2, 0)
        self.testInput2.setMove(1, 0)

        self.testInput1.setMove(0, 2)
        self.testInput2.setMove(1, 2)

        self.play.start()

        self.assertTupleEqual(tuple(), self.testRenderer.drawingPlayers)
        self.assertEqual(Mark.CIRCLE, self.testRenderer.winner.getMark())
        self.assertListEqual([(1, 0), (1, 1), (1, 2)], self.board.getWinningCells())

    def test_CrossWonGame(self):
        self.testInput1.setMove(0, 0)
        self.testInput2.setMove(1, 1)

        self.testInput1.setMove(2, 2)
        self.testInput2.setMove(2, 1)

        self.testInput1.setMove(0, 2)
        self.testInput2.setMove(1, 0)

        self.testInput1.setMove(0, 1)

        self.play.start()

        self.assertTupleEqual(tuple(), self.testRenderer.drawingPlayers)
        self.assertEqual(Mark.CROSS, self.testRenderer.winner.getMark())
        self.assertListEqual([(0, 0), (0, 1), (0, 2)], self.board.getWinningCells())
