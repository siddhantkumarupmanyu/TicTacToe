import copy
import math
from typing import Tuple

from Board import Board
from Cell import Mark
from Player import PlayerInputInterface


# todo: refactor and optimize this

class AIInput(PlayerInputInterface):

    def __init__(self, myMark: Mark, board: Board):
        self.board = board
        self.myMark = myMark
        if myMark == Mark.CIRCLE:
            self.opponentMark = Mark.CROSS
        else:
            self.opponentMark = Mark.CIRCLE

    def getMove(self) -> Tuple[int, int]:
        tempBoard = copy.deepcopy(self.board)
        value = self.getGoodValue(tempBoard)
        return value

    def getGoodValue(self, board: Board):
        children = self.getValues(board)
        maxEvalChild = children[0]
        maxEval = -math.inf
        for child in children:
            tempBoard = copy.deepcopy(board)
            tempBoard.setValueAt(child[0], child[1], self.myMark)
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
                tempBoard = copy.deepcopy(board)
                tempBoard.setValueAt(child[0], child[1], self.myMark)
                evaluated = self.minMax(tempBoard, False)
                maxEval = max(maxEval, evaluated)
            return maxEval - 1
        else:
            minEval = math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = copy.deepcopy(board)
                tempBoard.setValueAt(child[0], child[1], self.opponentMark)
                evaluated = self.minMax(tempBoard, True)
                minEval = min(minEval, evaluated)
            return minEval + 1

    def staticEvaluation(self, board: Board) -> float:
        if board.winner() == Mark.DEFAULT:
            return 0.0
        elif board.winner() == self.myMark:
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
