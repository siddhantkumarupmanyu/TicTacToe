from typing import Tuple

from Board import Board, Mark
from Player import Player, PlayerObserver
from Renderer import Renderer
from Require import Require


class Play(PlayerObserver):
    def __init__(self, player1: Player, player2: Player, board: Board, renderer: Renderer):
        Require.that(player1.getMark() != player2.getMark(), "Both Players have same Mark")
        self._player1 = player1
        self._player2 = player2
        self._board = board
        self._renderer = renderer
        self._player1.register(self)
        self._player2.register(self)
        self._player1.setMyMove(True)

    def moveEvent(self, move: Tuple[int, int]):
        currentPlayer = self._player1 if self._player1.isMyMove() else self._player2
        if not self._validMove(move[0], move[1]):
            self._renderer.invalidMove(currentPlayer, self._board, move)
            return

        self._board.setValueAt(move[0], move[1], currentPlayer.getMark())

        self._player1.setMyMove(not self._player1.isMyMove())
        self._player2.setMyMove(not self._player2.isMyMove())

        self._renderer.display(self._board, self._player1)

        if self._board.gameOver():
            self._gameOver()

    def _gameOver(self):
        winnerMark = self._board.winner()
        winner = None

        if winnerMark == Mark.DEFAULT:
            self._renderer.tie(self._board, self._player1, self._player2)
            return

        if self._player1.getMark() == winnerMark:
            winner = self._player1
        elif self._player2.getMark() == winnerMark:
            winner = self._player2

        self._renderer.won(self._board, winner)

    def _validMove(self, x: int, y: int):  # todo change to tuple
        if x > 2 or y > 2:
            return False
        if self._board.getValueAt(x, y) != Mark.DEFAULT:
            return False
        return True
