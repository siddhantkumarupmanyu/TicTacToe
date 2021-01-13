import math
from typing import Tuple

from Board import Board, Mark
from Player import Player


# todo: refactor and optimize this
# todo : fix this
class AIPlayer(Player):

    def __init__(self, mark: Mark, board: Board):
        super().__init__("AI Player", mark)
        self.board = board
        if mark == Mark.CIRCLE:
            self._opponentMark = Mark.CROSS
        else:
            self._opponentMark = Mark.CIRCLE

    def getMove(self) -> Tuple[int, int]:
        tempBoard = self.board.getNewBoardAtCurrentPosition()
        value = self.getGoodValue(tempBoard)
        return value

    # todo improve performance using coroutines/asyncio
    # run child no of coroutines and await for them to finish at the end and then compare values

    def getGoodValue(self, board: Board):
        children = self.getValues(board)
        maxEvalChild = children[0]
        maxEval = -math.inf
        for child in children:
            tempBoard = board.getNewBoardAtCurrentPosition()
            tempBoard.setValueAt(child[0], child[1], self._mark)
            evaluated = self.minMax(tempBoard, False)
            if evaluated > maxEval:
                maxEvalChild = child
            maxEval = max(maxEval, evaluated)
        return maxEvalChild

    def minMax(self, board: Board, maximizingPlayer):

        if board.gameOver():
            return self.staticEvaluation(board)

        if maximizingPlayer:
            maxEval = -math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._mark)
                evaluated = self.minMax(tempBoard, False)
                maxEval = max(maxEval, evaluated)
            return maxEval - 1
        else:
            minEval = math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._opponentMark)
                evaluated = self.minMax(tempBoard, True)
                minEval = min(minEval, evaluated)
            return minEval + 1

    def staticEvaluation(self, board: Board) -> float:
        if board.winner() == Mark.DEFAULT:
            return 0.0
        elif board.winner() == self._mark:
            return 10
        else:
            return -10

    def getValues(self, board):
        values = list()
        for i in range(3):
            for j in range(3):
                if board.getValueAt(i, j) == Mark.DEFAULT:
                    values.append((i, j))
        return values
