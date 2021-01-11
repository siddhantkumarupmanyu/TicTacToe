from typing import Tuple, List

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import clear

from AIInput import AIInput
from Board import Board
from Cell import Mark
from Play import Play
from Player import Player, PlayerInputInterface
from Renderer import Renderer


class ConsolePlayerInput(PlayerInputInterface):

    def getMove(self) -> Tuple[int, int]:
        move = self.parseInt(self.getInputFromConsole())
        if move == -1:
            return -1, -1
        elif move == 1:
            return 0, 0
        elif move == 2:
            return 0, 1
        elif move == 3:
            return 0, 2
        elif move == 4:
            return 1, 0
        elif move == 5:
            return 1, 1
        elif move == 6:
            return 1, 2
        elif move == 7:
            return 2, 0
        elif move == 8:
            return 2, 1
        elif move == 9:
            return 2, 2
        else:
            return -1, -1

    def getInputFromConsole(self) -> str:
        return input("Enter number between 0-8:- ")

    def parseInt(self, inputString):
        try:
            number = int(inputString)
            return number
        except ValueError:
            return -1


class ConsoleRenderer(Renderer):

    # todo refactor this

    def display(self, board: Board, nextMove: Player):
        clear()
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(0, 0))} | {self._getStringForMark(board.getValueAt(0, 1))} | {self._getStringForMark(board.getValueAt(0, 2))} \n")
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(1, 0))} | {self._getStringForMark(board.getValueAt(1, 1))} | {self._getStringForMark(board.getValueAt(1, 2))} \n")
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(2, 0))} | {self._getStringForMark(board.getValueAt(2, 1))} | {self._getStringForMark(board.getValueAt(2, 2))} \n")

    # todo:  refactor the code and remove as many hacks as possible; it does not matter in this class but still
    def won(self, board: Board, player: Player):
        clear()
        winningCells = board.getWinningCells()
        print_formatted_text(
            HTML(
                f"{self._getFormattedStringFor(board, 0, 0, winningCells)} | {self._getFormattedStringFor(board, 0, 1, winningCells)} | {self._getFormattedStringFor(board, 0, 2, winningCells)} \n"))
        print_formatted_text(
            HTML(
                f"{self._getFormattedStringFor(board, 1, 0, winningCells)} | {self._getFormattedStringFor(board, 1, 1, winningCells)} | {self._getFormattedStringFor(board, 1, 2, winningCells)} \n"))
        print_formatted_text(
            HTML(
                f"{self._getFormattedStringFor(board, 2, 0, winningCells)} | {self._getFormattedStringFor(board, 2, 1, winningCells)} | {self._getFormattedStringFor(board, 2, 2, winningCells)} \n"))
        print_formatted_text(HTML(f"Player <red>{player.getMark()}</red> has won the game!!!!\n"))

    def tie(self, board: Board, player1: Player, player2: Player):
        print(f"Tie!!!!\n")

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("You have entered a invalid move, please re-enter.")

    def _getFormattedStringFor(self, board, x: int, y: int, winningCells: List[Tuple[int, int]]):
        if (x, y) in winningCells:
            return f"<red>{self._getStringForMark(board.getValueAt(x, y))}</red>"
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
        renderer = ConsoleRenderer()
        board = Board()
        player1 = Player(Mark.CROSS, ConsolePlayerInput())
        player2 = Player(Mark.CIRCLE, AIInput(Mark.CIRCLE, board))

        play = Play(player1, player2, board, renderer)
        play.start()
