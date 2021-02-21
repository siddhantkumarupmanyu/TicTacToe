from typing import Tuple
from unittest import TestCase

from Board import Mark
from Player import Player, PlayerObserver


class TestObserver(PlayerObserver):
    def __init__(self):
        self.lastMove = tuple()

    def moveEvent(self, move: Tuple[int, int]):
        self.lastMove = move


class MyTestCase(TestCase):
    player: Player
    testObserver: TestObserver

    def setUp(self) -> None:
        global player
        global testObserver
        player = Player("TestPlayer", Mark.CROSS)
        testObserver = TestObserver()
        player.register(testObserver)

    def test_constructor(self):
        self.assertEqual("TestPlayer", player.getPlayerName())
        self.assertEqual(Mark.CROSS, player.getMark())

    def test_myMove(self):
        self.assertFalse(player.isMyMove())
        player.setMyMove(True)
        self.assertTrue(player.isMyMove())

    def test_playerMove(self):
        player.setMyMove(True)
        player.moveEvent((1, 1))
        self.assertTupleEqual((1, 1), testObserver.lastMove)
