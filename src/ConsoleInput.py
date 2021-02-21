from AIPlayer import AIPlayer
from Board import Mark
from Player import Player
from SimpleParser import SimpleParser


class ConsoleInput:
    def __init__(self):
        self._exit = False

    def run(self):
        while not self._exit:
            self._execute()

    def stop(self):
        self._exit = True

    def _execute(self):
        pass

    def _getMoveFromConsole(self):
        moveStr = input()
        moveStr = moveStr.strip()
        if ' ' in moveStr:
            moveSplit = moveStr.split()
            move = (int(moveSplit[0]), int(moveSplit[1]))
        else:
            move = SimpleParser.parseIntToTuple(int(moveStr))
        return move


class ConsoleInputTwoPlayers(ConsoleInput):
    def __init__(self, player1, player2):
        super().__init__()
        self._player1: Player = player1
        self._player2: Player = player2
        self._currentPlayer = self._player1

    def _execute(self):
        currentPlayer = self._player1 if self._player1.isMyMove() else self._player2
        move = self._getMoveFromConsole()
        currentPlayer.moveEvent(move)


class ConsoleInputSinglePlayer(ConsoleInput):
    def __init__(self, player, board):
        super().__init__()
        self._player: Player = player
        self._aiPlayer = AIPlayer(Mark.CIRCLE, board)

    def _execute(self):
        if self._player.isMyMove():
            move = self._getMoveFromConsole()
            self._player.moveEvent(move)
        else:
            move = self._aiPlayer.getMove()
            self._aiPlayer.moveEvent(move)

    def getAIPlayer(self) -> Player:
        return self._aiPlayer
