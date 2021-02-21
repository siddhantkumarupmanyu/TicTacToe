from typing import Tuple, List

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import clear

from AIPlayer import AIPlayer
from Board import Board, Mark
from Play import Play
from Player import Player
from Renderer import Renderer

gameEnded = False

invalidMove = False


class ConsoleRenderer(Renderer):

    # todo refactor this

    def displayBoard(self, board: Board, nextMove: Player):
        clear()
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(0, 0))} | {self._getStringForMark(board.getValueAt(0, 1))} | {self._getStringForMark(board.getValueAt(0, 2))} \n")
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(1, 0))} | {self._getStringForMark(board.getValueAt(1, 1))} | {self._getStringForMark(board.getValueAt(1, 2))} \n")
        print_formatted_text(
            f"{self._getStringForMark(board.getValueAt(2, 0))} | {self._getStringForMark(board.getValueAt(2, 1))} | {self._getStringForMark(board.getValueAt(2, 2))} \n")

    # todo:  refactor the code and remove as many hacks as possible; it does not matter in this class but still
    def displayWinner(self, board: Board, player: Player):
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
        global gameEnded
        gameEnded = True

    def tie(self, board: Board, player1: Player, player2: Player):
        print(f"Tie!!!!\n")
        global gameEnded
        gameEnded = True

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        print("You have entered a invalid move, please re-enter.")
        global invalidMove
        invalidMove = True

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


def parseInt(inputString):
    try:
        number = int(inputString)
        return number
    except ValueError:
        return -1


def getMove(string) -> Tuple[int, int]:
    move = parseInt(string)
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


class ConsoleInputTwoPlayers:

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def run(self):
        global invalidMove
        global gameEnded
        while True:
            player1Move = getMove(input(f"Enter move for {self.player1.getPlayerName()} :- "))
            while player1Move == (-1, -1):
                player1Move = getMove(input(f"Error Please Re-enter for {self.player1.getPlayerName()} :- "))
            self.player1.moveEvent(player1Move)

            while invalidMove:
                invalidMove = False
                player1Move = getMove(input(f"Error Please Re-enter for {self.player1.getPlayerName()} :- "))
                while player1Move == (-1, -1):
                    player1Move = getMove(input(f"Error Please Re-enter for {self.player1.getPlayerName()} :- "))
                self.player1.moveEvent(player1Move)

            if gameEnded:
                break

            player2Move = getMove(input(f"Enter move for {self.player2.getPlayerName()} :- "))
            while player2Move == (-1, -1):
                player2Move = getMove(input(f"Error Please Re-enter for {self.player2.getPlayerName()} :- "))
            self.player2.moveEvent(player2Move)

            while invalidMove:
                invalidMove = False
                player2Move = getMove(input(f"Error Please Re-enter for {self.player2.getPlayerName()} :- "))
                while player2Move == (-1, -1):
                    player2Move = getMove(input(f"Error Please Re-enter for {self.player2.getPlayerName()} :- "))
                self.player2.moveEvent(player2Move)

            if gameEnded:
                break


class ConsoleInputOnePlayerWithAI:

    def __init__(self, player: Player, aiPlayer: AIPlayer):
        self.player = player
        self.aiPlayer = aiPlayer

    def run(self):
        global invalidMove
        global gameEnded
        while True:
            playerMove = getMove(input(f"Enter move for {self.player.getPlayerName()} :- "))
            while playerMove == (-1, -1):
                playerMove = getMove(input(f"Error Please Re-enter for {self.player.getPlayerName()} :- "))
            self.player.moveEvent(playerMove)

            while invalidMove:
                invalidMove = False
                playerMove = getMove(input(f"Error Please Re-enter for {self.player.getPlayerName()} :- "))
                while playerMove == (-1, -1):
                    playerMove = getMove(input(f"Error Please Re-enter for {self.player.getPlayerName()} :- "))
                self.player.moveEvent(playerMove)

            if gameEnded:
                break

            move = self.aiPlayer.getMove()
            self.aiPlayer.moveEvent(move)

            if gameEnded:
                break


def startPlayers():
    renderer = ConsoleRenderer()
    board = Board()
    player1 = Player("Player 1", Mark.CROSS)
    player2 = Player("Player 2", Mark.CIRCLE)

    play = Play(player1, player2, board, renderer)

    consoleInput = ConsoleInputTwoPlayers(player1, player2)
    consoleInput.run()


def startAI():
    renderer = ConsoleRenderer()
    board = Board()
    player = Player("Player", Mark.CROSS)
    aiPlayer = AIPlayer(Mark.CIRCLE, board)

    play = Play(player, aiPlayer, board, renderer)

    consoleInput = ConsoleInputOnePlayerWithAI(player, aiPlayer)
    consoleInput.run()
