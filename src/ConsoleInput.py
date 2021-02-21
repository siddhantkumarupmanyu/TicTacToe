from AIPlayer import AIPlayer
from Board import Mark
from Player import Player


class ConsoleInput:
    def run(self):
        pass

    def stop(self):
        pass


class ConsoleInputTwoPlayers(ConsoleInput):
    def __init__(self, player1, player2):
        self._player1: Player = player1
        self._player2: Player = player2
        self._currentPlayer = self._player1
        self._exit = False

    def run(self):
        while not self._exit:
            currentPlayer = self._player1 if self._player1.isMyMove() else self._player2
            moveStr = input()
            moveSplit = moveStr.split()
            move = (int(moveSplit[0]), int(moveSplit[1]))
            currentPlayer.moveEvent(move)

    def stop(self):
        self._exit = True


class ConsoleInputSinglePlayer(ConsoleInput):
    def __init__(self, player, board):
        self._player: Player = player
        self._aiPlayer = AIPlayer(Mark.CIRCLE, board)
        self._exit = False

    def run(self):
        while not self._exit:
            if self._player.isMyMove():
                moveStr = input()
                moveSplit = moveStr.split()
                move = (int(moveSplit[0]), int(moveSplit[1]))
                self._player.moveEvent(move)
            else:
                move = self._aiPlayer.getMove()
                self._aiPlayer.moveEvent(move)

    def stop(self):
        self._exit = True

    def getAIPlayer(self) -> Player:
        return self._aiPlayer
