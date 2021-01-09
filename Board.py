from typing import List, Tuple

from Cell import Cell, Mark


# board class should be immutable
class Board:

    def __init__(self):
        self._matrix: List[List[Cell]] = list()
        self._defaultCell: Cell = Cell()
        self._winner: Mark = Mark.DEFAULT
        self._winningCells: List[Tuple[int, int]] = list()
        self.createMatrix()

    def createMatrix(self):
        tempMatrix = [
            [Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell()]
        ]
        self._matrix = tempMatrix

    def setValueAt(self, x: int, y: int, value: Mark):
        # # TODO: add fail fast for x & y > 3
        self._matrix[x][y].setValue(value)

    def getValueAt(self, x: int, y: int) -> Mark:
        # # TODO: add fail fast for x & y > 3
        return self._matrix[x][y].getValue()

    def winner(self) -> Mark:
        if self._winner is None:
            if not self.gameOver():  # # TODO: replace with fail fast code
                raise Exception("Game Is not over")
        return self._winner

    def getWinningCells(self) -> List[Tuple[int, int]]:
        if self._winningCells is None:
            if not self.gameOver():  # # TODO: replace with fail fast code
                raise Exception("Game Is not over")
        return self._winningCells

    def gameOver(self) -> bool:
        for i in range(3):
            if self._checkIfRowCellsAreEqual(i):
                self._winner = self._matrix[i][0].getValue()
                return True

            elif self._checkIfColumnCellsAreEqual(i):
                self._winner = self._matrix[0][i].getValue()
                return True

        if self._checkIfDiagonalCellsEqual():
            self._winner = self._matrix[1][1].getValue()
            return True

        if self._isGameDraw():
            self._winner = Mark.DEFAULT
            return True

        return False

    # TODO: I think setting winning cells do not belong to these checking methods
    # but if here where and how
    # may be the function name can be a bit more clear to express what they does

    def _checkIfRowCellsAreEqual(self, rowNum: int) -> bool:
        if self._defaultCell != self._matrix[rowNum][0] == self._matrix[rowNum][1] == self._matrix[rowNum][2]:
            self._winningCells = [(rowNum, 0), (rowNum, 1), (rowNum, 2)]
            return True
        return False

    def _checkIfColumnCellsAreEqual(self, colNum: int) -> bool:
        if self._defaultCell != self._matrix[0][colNum] == self._matrix[1][colNum] == self._matrix[2][colNum]:
            self._winningCells = [(0, colNum), (1, colNum), (2, colNum)]
            return True
        return False

    def _checkIfDiagonalCellsEqual(self) -> bool:
        if self._defaultCell != self._matrix[0][0] == self._matrix[1][1] == self._matrix[2][2]:
            self._winningCells = [(0, 0), (1, 1), (2, 2)]
            return True
        elif self._defaultCell != self._matrix[1][2] == self._matrix[1][1] == self._matrix[2][1]:
            self._winningCells = [(1, 2), (1, 1), (2, 1)]
            return True
        return False

    def _isGameDraw(self):
        if self.isFull():
            return True
        return False

    def isFull(self):
        for i in range(3):
            for j in range(3):
                if self._matrix[i][j].getValue() == Mark.DEFAULT:
                    return False
        return True

    def isEmpty(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self._matrix[i][j].getValue() != Mark.DEFAULT:
                    return False
        return True
