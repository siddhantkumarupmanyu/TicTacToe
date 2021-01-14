import asyncio
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
        # value = self.getGoodValue(tempBoard)
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(self.getGoodValue(tempBoard))
        return value

    # todo improve performance using coroutines/asyncio
    # run child no of coroutines and await for them to finish at the end and then compare values
    # event loop with work for our case as we only want synchronous execution

    async def getGoodValue(self, board: Board):
        children = self.getValues(board)
        # maxEvalChild = children[0]
        maxEval = -math.inf
        coroutines = list()
        for child in children:
            tempBoard = board.getNewBoardAtCurrentPosition()
            tempBoard.setValueAt(child[0], child[1], self._mark)
            coroutines.append(self.minMax(tempBoard, False))
            # if evaluated > maxEval:
            #     maxEvalChild = child
            # maxEval = max(maxEval, evaluated)
        evaluated = await asyncio.gather(*coroutines)
        maxChildIndex = 0
        for i, evaluation in enumerate(evaluated):
            if evaluation > maxEval:
                maxEval = evaluation
                maxChildIndex = i
        return children[maxChildIndex]

    async def minMax(self, board: Board, maximizingPlayer):

        if board.gameOver():
            return await self.staticEvaluation(board)

        if maximizingPlayer:
            maxEval = -math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._mark)
                evaluated = await self.minMax(tempBoard, False)
                maxEval = max(maxEval, evaluated)
            return maxEval - 1
        else:
            minEval = math.inf
            children = self.getValues(board)
            for child in children:
                tempBoard = board.getNewBoardAtCurrentPosition()
                tempBoard.setValueAt(child[0], child[1], self._opponentMark)
                evaluated = await self.minMax(tempBoard, True)
                minEval = min(minEval, evaluated)
            return minEval + 1

    async def staticEvaluation(self, board: Board):
        if board.winner() == Mark.DEFAULT:
            return 0
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


if __name__ == '__main__':
    import time
    import random

    current_milli_time = lambda: int(round(time.time() * 1000))


    def _benchmarkSecond():
        print("Ai is Second in turn")

        board = Board()
        aiPlayer = AIPlayer(Mark.CIRCLE, board)

        board.setValueAt(random.randint(0, 2), random.randint(0, 2), aiPlayer.getMark())

        oldTime = current_milli_time()

        move = aiPlayer.getMove()

        print(f"Took {current_milli_time() - oldTime} ms")
        print(f"move = {move}")


    def _benchmarkFirst():
        # does not make any sense will always return same value
        # so can just store it
        pass


    _benchmarkSecond()
