import os
from typing import Tuple, List

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

    def _displayBoard(self, board, winningCells=None):
        self._clearScreen()
        for i in range(0, 3):
            winningCellsInRow = self._getWinningCellsInRow(i, winningCells)
            self._displayLine(board.getValueAt(i, 0), board.getValueAt(i, 1), board.getValueAt(i, 2), winningCellsInRow)
            if i < 2:
                self._displayHorizontalLine()

    def _getWinningCellsInRow(self, row, winningCells) -> List:
        positions = list()
        if winningCells is None:
            positions.append(False)
            positions.append(False)
            positions.append(False)
            return positions
        for i in range(0, 3):
            if ((row, i) == winningCells[0]) or ((row, i) == winningCells[1]) or ((row, i) == winningCells[2]):
                positions.append(True)
            else:
                positions.append(False)
        return positions

    def displayWinner(self, board: Board, player: Player):
        self._displayBoard(board, board.getWinningCells())
        print(f"Winner Is: {self._getIconFromMark(player.getMark())}")
        self._consoleInput.stop()

    def tie(self, board: Board, player1: Player, player2: Player):
        print("\n")
        print(
            f"Its a TIE between {self._getIconFromMark(player1.getMark())} and {self._getIconFromMark(player2.getMark())}"
        )
        self._consoleInput.stop()

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("Invalid Move\n")

    def _displayLine(self, a, b, c, winningCellsInLine: List):
        aMark = self._getIconFromMark(a)
        bMark = self._getIconFromMark(b)
        cMark = self._getIconFromMark(c)
        print(
            f"{self._formatWinningCell(aMark, winningCellsInLine[0])} | {self._formatWinningCell(bMark, winningCellsInLine[1])} | {self._formatWinningCell(cMark, winningCellsInLine[2])}"
        )

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

    def _formatWinningCell(self, aMark, value):
        if value:
            return f"'{aMark}'"
        return aMark
