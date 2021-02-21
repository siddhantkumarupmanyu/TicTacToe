from Board import Board, Mark
from ConsoleInput import ConsoleInputTwoPlayers, ConsoleInputSinglePlayer
from ConsoleRenderer import ConsoleRenderer
from Play import Play
from Player import Player


def startPlayers():
    board = Board()
    player1 = Player("Player 1", Mark.CROSS)
    player2 = Player("Player 2", Mark.CIRCLE)

    consoleInput = ConsoleInputTwoPlayers(player1, player2)
    renderer = ConsoleRenderer(consoleInput)
    play = Play(player1, player2, board, renderer)

    consoleInput.run()


def startAI():
    board = Board()
    player = Player("Player 1", Mark.CROSS)

    consoleInput = ConsoleInputSinglePlayer(player, board)
    renderer = ConsoleRenderer(consoleInput)
    play = Play(player, consoleInput.getAIPlayer(), board, renderer)

    consoleInput.run()
