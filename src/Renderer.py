from typing import Tuple

from Board import Board
from Player import Player


class Renderer:
    def display(self, board: Board, nextMove: Player):
        pass

    def won(self, board: Board, player: Player):
        pass

    def tie(self, board: Board, player1: Player, player2: Player):
        pass

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        pass
