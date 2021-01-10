from typing import Tuple
from unittest import TestCase

from Cell import Mark
from Player import Player, PlayerInputInterface


class TestPlayerInput(PlayerInputInterface):
    _move: Tuple[int, int] = (0, 0)

    def setMove(self, x: int, y: int):
        self._move = (x, y)

    def setMoveTuple(self, xy: Tuple[int, int]):
        self._move = xy

    def getMove(self) -> Tuple[int, int]:
        return self._move


class TestPlayer(TestCase):

    def test_CreatePlayerWithItsCellValue(self):
        testInput = TestPlayerInput()
        player = Player(Mark.CROSS, testInput)
        self.assertEqual(Mark.CROSS, player.getMark())
        player2 = Player(Mark.CIRCLE, testInput)
        self.assertEqual(Mark.CIRCLE, player2.getMark())

    def test_playerGetMove(self):
        testInput = TestPlayerInput()
        player = Player(Mark.CROSS, testInput)
        testInput.setMove(0, 0)
        self.assertEqual((0, 0), player.getMove())
        testInput.setMove(2, 0)
        self.assertEqual((2, 0), player.getMove())
        testInput.setMove(1, 2)
        self.assertEqual((1, 2), player.getMove())
