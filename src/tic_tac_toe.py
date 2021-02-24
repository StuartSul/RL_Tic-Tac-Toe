from config import Config
from src.ai.ai import AI
from src.engine.board import Board
from src.gui.gui import GUI
from time import sleep

def run():
    board = Board(size=Config.SIZE, silent=Config.SILENT)

    if Config.AI_WHITE_ENABLE or Config.AI_BLACK_ENABLE:
        ai = AI(board)

    if Config.GUI:
        GUI(board)
    elif Config.TRAIN_WHITE or Config.TRAIN_BLACK:
        while True:
            sleep

    if Config.AI_WHITE_ENABLE or Config.AI_BLACK_ENABLE:
        ai.stop()

    quit(0)
