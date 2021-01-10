from enum import Enum


class Mark(Enum):
    CIRCLE = -1
    DEFAULT = 0
    CROSS = 1


class Cell:

    def __init__(self):
        self._value: Mark = Mark.DEFAULT
        self._isEmpty = True

    def setValue(self, value: Mark):
        if not self._isEmpty:
            raise Exception("Cell is Already filled")  # TODO: replace with fail fast code
        self._value = value
        self._isEmpty = False

    def getValue(self) -> Mark:
        return self._value

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cell):
            return self._value == o._value
        else:
            return False

    def __ne__(self, o: object):
        if isinstance(o, Cell):
            return self._value != o._value
        else:
            return True

    def __hash__(self):
        return hash(self._value)  # TODO: check weather this returns same hash for same objects
