import math
from typing import Tuple

from Board import Board, Mark
from Player import Player


# todo: refactor and optimize this
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

    def getGoodValue(self, board: Board):
        children = self.getValues(board)
        maxEval = -math.inf
        evaluated = list()
        for child in children:
            tempBoard = board.getNewBoardAtCurrentPosition()
            tempBoard.setValueAt(child[0], child[1], self._mark)
            evaluated.append(self.minMax(tempBoard, False, 0))

        maxChildIndex = 0
        for i, evaluation in enumerate(evaluated):
            if evaluation > maxEval:
                maxChildIndex = i
                maxEval = evaluation

        maxEvalChild = children[maxChildIndex]

        return maxEvalChild

    def minMax(self, board: Board, maximizingPlayer: bool, depth: int):

        if board.gameOver():
            return self.staticEvaluation(board, depth)

        if maximizingPlayer:
            maxEval = -math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._mark)
                evaluated = self.minMax(tempBoard, False, depth + 1)
                maxEval = max(maxEval, evaluated)
            return maxEval
        else:
            minEval = math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._opponentMark)
                evaluated = self.minMax(tempBoard, True, depth + 1)
                minEval = min(minEval, evaluated)
            return minEval

    def staticEvaluation(self, board: Board, depth: int):
        if board.winner() == Mark.DEFAULT:
            return 0.0
        elif board.winner() == self._mark:
            return 10 - depth
        else:
            return -10 + depth

    def getValues(self, board):
        values = list()
        for i in range(3):
            for j in range(3):
                if board.getValueAt(i, j) == Mark.DEFAULT:
                    values.append((i, j))
        return values


if __name__ == '__main__':
    import time
    import random

    current_milli_time = lambda: int(round(time.time() * 1000))


    def _benchmarkSecond():
        print("Ai is Second in turn")

        board = Board()
        aiPlayer = AIPlayer(Mark.CIRCLE, board)

        board.setValueAt(random.randint(0, 2), random.randint(0, 2), Mark.CROSS)

        oldTime = current_milli_time()

        move = aiPlayer.getMove()

        print(f"Took {current_milli_time() - oldTime} ms")
        print(f"move = {move}")


    def _benchmarkFirst():
        # does not make any sense will always return same value
        # so can just store it
        pass


    _benchmarkSecond()
