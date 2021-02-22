from AIPlayer import AIPlayer
from Board import Mark
from Player import Player


class GuiInput:
    def __init__(self, player, board):
        self._player: Player = player
        self._aiPlayer = AIPlayer(Mark.CIRCLE, board)

    def getAIPlayer(self) -> Player:
        return self._aiPlayer

    def buttonClicked(self, row, col, gameOver: bool):
        if not gameOver:
            self._player.moveEvent((row, col))
            move = self._aiPlayer.getMove()
            self._aiPlayer.moveEvent(move)
