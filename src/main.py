import sys

from Game import startPlayers, startGui

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-p':
        startPlayers()
    else:
        # startAI()
        startGui()
