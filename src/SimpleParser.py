from typing import Tuple


class SimpleParser:

    @staticmethod
    def parseIntToTuple(n: int) -> Tuple[int, int]:
        n -= 1
        row = n // 3
        col = (n % 3)
        return (row, col)
