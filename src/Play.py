from Board import Board
from Cell import Mark
from Player import Player
from Renderer import Renderer


class Play:

    def __init__(self, player1: Player, player2: Player, board: Board, renderer: Renderer):

        # TODO: fail fast when player1.mark == player2.mark or any mark is default

        self._player1 = player1
        self._player2 = player2
        self._board = board
        self._renderer = renderer

    def start(self):
        # TODO refactor this into smaller methods/ functions
        self._renderer.display(self._board, self._player1)
        while True:
            p1X, p1Y = self._player1.getMove()
            while not self._validMove(p1X, p1Y):
                self._renderer.invalidMove(self._player1, self._board, (p1X, p1Y))
                p1X, p1Y = self._player1.getMove()

            self._board.setValueAt(p1X, p1Y, self._player1.getMark())

            self._renderer.display(self._board, self._player2)

            if self._board.gameOver():
                self._gameOver()
                break

            p2X, p2Y = self._player2.getMove()
            while not self._validMove(p2X, p2Y):
                self._renderer.invalidMove(self._player2, self._board, (p2X, p2Y))
                p2X, p2Y = self._player2.getMove()
            self._board.setValueAt(p2X, p2Y, self._player2.getMark())

            self._renderer.display(self._board, self._player1)

            if self._board.gameOver():
                self._gameOver()
                break

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

    def _validMove(self, x: int, y: int):
        if x > 2 or y > 2:
            return False
        if self._board.getValueAt(x, y) != Mark.DEFAULT:
            return False
        return True
