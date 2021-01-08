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
        while True:
            p1X, p1Y = self._player1.getMove()
            self._board.setValueAt(p1X, p1Y, self._player1.getMark())

            if self._board.gameOver():
                self._gameOver()
                break

            self._renderer.display(self._board, self._player2)

            p2X, p2Y = self._player2.getMove()
            self._board.setValueAt(p2X, p2Y, self._player2.getMark())

            if self._board.gameOver():
                self._gameOver()
                break

            self._renderer.display(self._board, self._player1)

    def _gameOver(self):
        winnerMark = self._board.winner()
        winner = None

        if winnerMark == Mark.DEFAULT:
            self._renderer.draw(self._board, self._player1, self._player2)
        elif self._player1.getMark() == winnerMark:
            winner = self._player1
        elif self._player2.getMark() == winnerMark:
            winner = self._player2

        self._renderer.won(self._board, winner)
