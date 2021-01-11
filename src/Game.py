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
        os.system('clear')
        print(
            f"{self._getStringForMark(board.getValueAt(0, 0))} | {self._getStringForMark(board.getValueAt(0, 1))} | {self._getStringForMark(board.getValueAt(0, 2))} \n")
        print(
            f"{self._getStringForMark(board.getValueAt(1, 0))} | {self._getStringForMark(board.getValueAt(1, 1))} | {self._getStringForMark(board.getValueAt(1, 2))} \n")
        print(
            f"{self._getStringForMark(board.getValueAt(2, 0))} | {self._getStringForMark(board.getValueAt(2, 1))} | {self._getStringForMark(board.getValueAt(2, 2))} \n")

    # todo:  refactor the code and remove as many hacks as possible; it does not matter in this class but still
    def won(self, board: Board, player: Player):
        os.system('clear')
        winningCells = board.getWinningCells()
        os.system(
            f'echo "{self._getFormattedStringFor(board, 0, 0, winningCells)} | {self._getFormattedStringFor(board, 0, 1, winningCells)} | {self._getFormattedStringFor(board, 0, 2, winningCells)}"')
        os.system('echo ""')
        os.system(
            f'echo "{self._getFormattedStringFor(board, 1, 0, winningCells)} | {self._getFormattedStringFor(board, 1, 1, winningCells)} | {self._getFormattedStringFor(board, 1, 2, winningCells)}"')
        os.system('echo ""')
        os.system(
            f'echo "{self._getFormattedStringFor(board, 2, 0, winningCells)} | {self._getFormattedStringFor(board, 2, 1, winningCells)} | {self._getFormattedStringFor(board, 2, 2, winningCells)}"')
        os.system('echo ""')
        print(f"Player {player.getMark()} has won the game!!!!\n")

    def tie(self, board: Board, player1: Player, player2: Player):
        print(f"Tie!!!!\n")

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("You have entered a invalid move, please re-enter.")

    def _getFormattedStringFor(self, board, x: int, y: int, winningCells: List[Tuple[int, int]]) -> str:
        if (x, y) in winningCells:
            return f"\e[7m{self._getStringForMark(board.getValueAt(x, y))}\e[27m"
        else:
            return self._getStringForMark(board.getValueAt(x, y))

    @staticmethod
    def _getStringForMark(mark: Mark) -> str:
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
