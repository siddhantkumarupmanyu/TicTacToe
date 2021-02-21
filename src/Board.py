import copy
from enum import Enum
from typing import List, Tuple, Optional

from Require import Require


class Mark(Enum):
    CIRCLE = -1
    DEFAULT = 0
    CROSS = 1


# todo make board class immutable
class Board:

    def __init__(self):
        self._createMatrix()
        self._winner: Optional[Mark] = None
        self._winningCells: List[Tuple[int, int]] = list()

    def getValueAt(self, x: int, y: int) -> Mark:
        Require.that(x < 3 and y < 3, f"Value should be less than 3 is X=[{x}] Y=[{y}]")
        return self._matrix[x][y]

    def setValueAt(self, x: int, y: int, value: Mark):
        Require.that(x < 3 and y < 3, f"Value should be less than 3 is X=[{x}] Y=[{y}]")
        Require.that(self._matrix[x][y] == Mark.DEFAULT, "Cell should be Empty")
        self._matrix[x][y] = value

    def winner(self) -> Mark:
        if self._winner is None:
            Require.that(self.gameOver(), "Game Is not over")
        return self._winner

    def getWinningCells(self) -> List[Tuple[int, int]]:
        if len(self._winningCells) == 0:
            Require.that(self.gameOver(), "Game Is not over")
        return self._winningCells

    def gameOver(self) -> bool:
        for i in range(3):
            if self._checkIfRowCellsAreEqual(i):
                self._winner = self._matrix[i][0]
                return True

            elif self._checkIfColumnCellsAreEqual(i):
                self._winner = self._matrix[0][i]
                return True

        if self._checkIfDiagonalCellsEqual():
            self._winner = self._matrix[1][1]
            return True

        if self._isGameDraw():
            self._winner = Mark.DEFAULT
            return True

        return False

    # TODO: I think setting winning cells do not belong to these checking methods
    # but if here where and how
    # may be the function name can be a bit more clear to express what they does

    def _checkIfRowCellsAreEqual(self, rowNum: int) -> bool:
        if Mark.DEFAULT != self._matrix[rowNum][0] == self._matrix[rowNum][1] == self._matrix[rowNum][2]:
            self._winningCells = [(rowNum, 0), (rowNum, 1), (rowNum, 2)]
            return True
        return False

    def _checkIfColumnCellsAreEqual(self, colNum: int) -> bool:
        if Mark.DEFAULT != self._matrix[0][colNum] == self._matrix[1][colNum] == self._matrix[2][colNum]:
            self._winningCells = [(0, colNum), (1, colNum), (2, colNum)]
            return True
        return False

    def _checkIfDiagonalCellsEqual(self) -> bool:
        if Mark.DEFAULT != self._matrix[0][0] == self._matrix[1][1] == self._matrix[2][2]:
            self._winningCells = [(0, 0), (1, 1), (2, 2)]
            return True
        elif Mark.DEFAULT != self._matrix[0][2] == self._matrix[1][1] == self._matrix[2][0]:
            self._winningCells = [(0, 2), (1, 1), (2, 0)]
            return True
        return False

    def _isGameDraw(self):
        if self.isFull():
            return True
        return False

    def isFull(self):
        for i in range(3):
            for j in range(3):
                if self._matrix[i][j] == Mark.DEFAULT:
                    return False
        return True

    def isEmpty(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self._matrix[i][j] != Mark.DEFAULT:
                    return False
        return True

    def getNewBoardAtCurrentPosition(self) -> 'Board':
        return copy.deepcopy(self)

    def _createMatrix(self):
        tempMatrix = [
            [Mark.DEFAULT, Mark.DEFAULT, Mark.DEFAULT],
            [Mark.DEFAULT, Mark.DEFAULT, Mark.DEFAULT],
            [Mark.DEFAULT, Mark.DEFAULT, Mark.DEFAULT]
        ]
        self._matrix = tempMatrix
