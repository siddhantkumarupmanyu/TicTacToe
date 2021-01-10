from typing import Tuple

from Cell import Mark


# interface for getting input from different type of sources
class PlayerInputInterface:
    def getMove(self) -> Tuple[int, int]:
        pass


class Player:

    def __init__(self, cellValue: Mark, playerInput: PlayerInputInterface):
        self._cellValue = cellValue
        self._playerInput = playerInput

    def getMark(self) -> Mark:
        return self._cellValue

    def getMove(self) -> Tuple[int, int]:
        return self._playerInput.getMove()
