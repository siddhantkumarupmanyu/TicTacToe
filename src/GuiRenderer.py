import tkinter as tk
from typing import Tuple

from Board import Board, Mark
from GuiInput import GuiInput
from Player import Player
from Renderer import Renderer
from SimpleParser import SimpleParser


class GuiRenderer(Renderer):
    def __init__(self, input: GuiInput):
        self._buttons = None
        self._window = tk.Tk()
        self._buttonsFrame = tk.Frame(self._window)
        self._setUpGui()
        self._input = input
        self._gameOver = False

    def _setUpGui(self):
        self._buttons = list()
        for i in range(3):
            self._buttonsFrame.columnconfigure(i, weight=1, minsize=75)
            self._buttonsFrame.rowconfigure(i, weight=1, minsize=50)
            for j in range(3):
                button = tk.Button(
                    master=self._buttonsFrame,
                    text=f"X",
                    command=lambda row=i, col=j: self._input.buttonClicked(row, col, self._gameOver)
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self._buttons.append(button)
        self._buttonsFrame.pack(fill=tk.BOTH, expand=True)
        self._label = tk.Label(self._window, text=" ", foreground="red")
        self._label.pack(fill=tk.X)

    def runGui(self):
        self._window.mainloop()

    def displayBoardWithNextMove(self, board: Board, nextMove: Player):
        for i, button in enumerate(self._buttons):
            cell = SimpleParser.parseIntToTuple(i + 1)
            value = self._getIconFromMark(board.getValueAt(cell[0], cell[1]))
            button['text'] = value

    def displayWinner(self, board: Board, player: Player):
        self._label['text'] = f"{player.getMark()} won"
        self._gameOver = True

    def tie(self, board: Board, player1: Player, player2: Player):
        self._label['text'] = f"It's a Tie"
        self._gameOver = True

    def invalidMove(self, player: Player, board: Board, move: Tuple[int, int]):
        self._label['text'] = f"invalid Move Entered"

    def _getIconFromMark(self, a: Mark):
        if a == Mark.CROSS:
            return "X"
        elif a == Mark.CIRCLE:
            return "O"
        else:
            return " "
