from typing import List

from Cell import Cell, Mark

# CROSS = "X"
# CIRCLE = "O"


# board class should be immutable
class Board:
    _matrix: List[List[Cell]]
    _defaultCell: Cell = Cell()

    # I think winning related stuff should be in different class. I thing Board is doing more than one thing
    _winner: Mark = None
    _winningCells: List[Cell] = None

    def __init__(self):
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

    def winner(self):
        if self._winner is None:
            if not self.gameOver():  # # TODO: replace with fail fast code
                raise Exception("Game Is not over")
        return self._winner

    def getWinningCells(self) -> List[Cell]:
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
            self._winningCells = [self._matrix[rowNum][0], self._matrix[rowNum][1], self._matrix[rowNum][2]]
            return True
        return False

    def _checkIfColumnCellsAreEqual(self, colNum: int) -> bool:
        if self._defaultCell != self._matrix[0][colNum] == self._matrix[1][colNum] == self._matrix[2][colNum]:
            self._winningCells = [self._matrix[0][colNum], self._matrix[1][colNum], self._matrix[2][colNum]]
            return True
        return False

    def _checkIfDiagonalCellsEqual(self) -> bool:
        if self._defaultCell != self._matrix[0][0] == self._matrix[1][1] == self._matrix[2][2]:
            self._winningCells = [self._matrix[0][0], self._matrix[1][1], self._matrix[2][2]]
            return True
        elif self._defaultCell != self._matrix[1][2] == self._matrix[1][1] == self._matrix[2][1]:
            self._winningCells = [self._matrix[1][2], self._matrix[1][1], self._matrix[2][1]]
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
