import threading

from AIPlayer import AIPlayer
from Board import Mark
from Player import Player


class GuiInput:
    def __init__(self, player, board):
        self._player: Player = player
        self._aiPlayer = AIPlayer(Mark.CIRCLE, board)

    def getAIPlayer(self) -> Player:
        return self._aiPlayer

    def _getAiMove(self):
        move = self._aiPlayer.getMove()
        if not self._gameOver(move):
            self._aiPlayer.moveEvent(move)

    def _gameOver(self, move) -> bool:
        return move == (-1, -1)

    def buttonClicked(self, row, col, gameOver: bool):
        if not gameOver:
            self._player.moveEvent((row, col))
            thread = threading.Thread(target=self._getAiMove)
            thread.start()
