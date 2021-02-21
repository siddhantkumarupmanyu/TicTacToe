from typing import List, Tuple

from Board import Mark
from Require import Require


class PlayerObserver:
    def moveEvent(self, move: Tuple[int, int]):
        pass


class Player:

    def __init__(self, playerName: str, mark: Mark):
        Require.that(mark != Mark.DEFAULT, "Player Mark should not be Mark.DEFAULT")
        self._mark = mark
        self._playerName = playerName
        self._myMove = False
        self._observers: List[PlayerObserver] = list()

    def setMyMove(self, myMove: bool):
        self._myMove = myMove

    def isMyMove(self) -> bool:
        return self._myMove

    def moveEvent(self, move: Tuple[int, int]):
        if self._myMove:
            self._notify(move)

    def getMark(self) -> Mark:
        return self._mark

    def getPlayerName(self):
        return self._playerName

    def register(self, observer: PlayerObserver):
        self._observers.append(observer)

    def _notify(self, move: Tuple[int, int]):
        for observer in self._observers:
            observer.moveEvent(move)
