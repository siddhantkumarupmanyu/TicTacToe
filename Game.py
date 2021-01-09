import os
from typing import Tuple, List

from Board import Board
from Cell import Mark
from Play import Play
from Player import Player, PlayerInputInterface
from Renderer import Renderer


class ConsolePlayerInput(PlayerInputInterface):

    def getMove(self) -> Tuple[int, int]:
        string = self.getInputFromConsole()
        while len(string) == 1:
            print("Enter x and y Both")
            string = self.getInputFromConsole()

        while not self.parseInt(string)[1]:
            string = self.getInputFromConsole()

        return self.parseInt(string)[0]

    def getInputFromConsole(self) -> List[str]:
        playerInput = input("Enter x y:- ")
        string = playerInput.strip().split()

        return string

    def parseInt(self, inputString):
        try:
            x = int(inputString[0])
            y = int(inputString[1])
            return ((x, y), True)
        except ValueError:
            return ((-1, -1), False)


class ConsoleRenderer(Renderer):

    # todo refactor this

    def display(self, board: Board, nextMove: Player):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
            f"{self._getStringForMark(board.getValueAt(0, 0))} | {self._getStringForMark(board.getValueAt(0, 1))} | {self._getStringForMark(board.getValueAt(0, 2))} \n")
        print(
            f"{self._getStringForMark(board.getValueAt(1, 0))} | {self._getStringForMark(board.getValueAt(1, 1))} | {self._getStringForMark(board.getValueAt(1, 2))} \n")
        print(
            f"{self._getStringForMark(board.getValueAt(2, 0))} | {self._getStringForMark(board.getValueAt(2, 1))} | {self._getStringForMark(board.getValueAt(2, 2))} \n")

    def won(self, board: Board, player: Player):
        # todo: add strike through here for winning cells
        self.display(board, player)
        print(f"Player {player.getMark()} has won the game!!!!\n")

    def draw(self, board: Board, player1: Player, player2: Player):
        print(f"Tie!!!!\n")

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("You have entered a invalid move, please re-enter.")

    def _getStringForMark(self, mark: Mark) -> str:
        if mark == Mark.CROSS:
            return "X"
        elif mark == Mark.CIRCLE:
            return "O"
        else:
            return " "


class Game:

    def start(self):
        player1 = Player(Mark.CROSS, ConsolePlayerInput())
        player2 = Player(Mark.CIRCLE, ConsolePlayerInput())

        renderer = ConsoleRenderer()
        board = Board()
        play = Play(player1, player2, board, renderer)
        play.start()
