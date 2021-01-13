from typing import List, Tuple

from Cell import Mark


class PlayerObserver:
    def moveEvent(self, move: Tuple[int, int]):
        pass


class PlayerSubject:
    def __init__(self):
        self._observers: List[PlayerObserver] = list()

    def register(self, observer: PlayerObserver):
        self._observers.append(observer)

    def notify(self, move: Tuple[int, int]):
        for observer in self._observers:
            observer.moveEvent(move)


# i can test this but this class does not have too much things to test
# leaving it for now
class Player(PlayerSubject):

    def __init__(self, playerName: str, mark: Mark):
        super().__init__()
        self._mark = mark
        self._playerName = playerName
        self._myMove = False

    def setMyMove(self, myMove: bool):
        self._myMove = myMove

    def isMyMove(self) -> bool:
        return self._myMove

    def moveEvent(self, move):
        if self._myMove:
            self.notify(move)

    def getMark(self) -> Mark:
        return self._mark

    def getPlayerName(self):
        return self._playerName
