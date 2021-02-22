from src.engine.board import Board
from src.gui.gui import GUI

SIZE = 3

def run():
    board = Board(size=SIZE)
    GUI(board)
    quit(0)
