from config import Config
from src.ai.ai import AI
from src.engine.board import Board
from src.gui.gui import GUI
from time import sleep

AI_ENABLED = Config.AI_WHITE_ENABLE or Config.AI_BLACK_ENABLE
AI_TRAINING = Config.TRAIN_WHITE or Config.TRAIN_BLACK

def run():
    board = Board(size=Config.SIZE, silent=Config.SILENT)
    
    if AI_ENABLED:
        ai = AI(board)
        if Config.AI_WHITE_ENABLE:
            ai.load(board.WHITE_TURN, Config.AI_WHITE_ALGORITHM)
        if Config.AI_BLACK_ENABLE:
            ai.load(board.BLACK_TURN, Config.AI_BLACK_ALGORITHM)
        ai.start()

    if Config.GUI:
        GUI(board)
    elif AI_TRAINING:
        while True:
            sleep(1)
        
    if AI_ENABLED:
        ai.stop()

    quit(0)
