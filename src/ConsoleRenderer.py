import os
from typing import Tuple

from Board import Board, Mark
from ConsoleInput import ConsoleInput
from Player import Player
from Renderer import Renderer


class ConsoleRenderer(Renderer):
    def __init__(self, consoleInput: ConsoleInput):
        self._consoleInput = consoleInput

    def displayBoardWithNextMove(self, board: Board, nextMove: Player):
        self._displayBoard(board)
        self._askNextMove(nextMove)

    def _displayBoard(self, board):
        self._clearScreen()
        self._displayLine(board.getValueAt(0, 0), board.getValueAt(0, 1), board.getValueAt(0, 2))
        self._displayHorizontalLine()
        self._displayLine(board.getValueAt(1, 0), board.getValueAt(1, 1), board.getValueAt(1, 2))
        self._displayHorizontalLine()
        self._displayLine(board.getValueAt(2, 0), board.getValueAt(2, 1), board.getValueAt(2, 2))

    def displayWinner(self, board: Board, player: Player):
        self._displayBoard(board)
        print(f"Winner Is: {self._getIconFromMark(player.getMark())}")
        self._consoleInput.stop()

    def tie(self, board: Board, player1: Player, player2: Player):
        print(
            f"Its a TIE between {self._getIconFromMark(player1.getMark())} and {self._getIconFromMark(player2.getMark())}"
        )
        self._consoleInput.stop()

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("Invalid Move\n")

    def _displayLine(self, a, b, c):
        print(f"{self._getIconFromMark(a)} | {self._getIconFromMark(b)} | {self._getIconFromMark(c)}")

    def _clearScreen(self):
        print(end='\n')
        os.system("clear")

    def _displayHorizontalLine(self):
        print("---------")

    def _askNextMove(self, player):
        print(f"{self._getIconFromMark(player.getMark())} enter move:- ", end='')

    def _getIconFromMark(self, a: Mark):
        if a == Mark.CROSS:
            return "X"
        elif a == Mark.CIRCLE:
            return "O"
        else:
            return " "
