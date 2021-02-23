from config import Config
from src.ai.ai import AI
from src.engine.board import Board
from src.gui.gui import GUI

AI_ENABLED = Config.AI_WHITE_ENABLE or Config.AI_BLACK_ENABLE

def run():
    board = Board(size=Config.SIZE)
    
    if AI_ENABLED:
        ai = AI(board)
        if Config.AI_WHITE_ENABLE:
            ai.load(board.WHITE_TURN, Config.AI_WHITE_ALGORITHM)
        if Config.AI_BLACK_ENABLE:
            ai.load(board.BLACK_TURN, Config.AI_BLACK_ALGORITHM)
        ai.start()

    GUI(board)

    if AI_ENABLED:
        ai.stop()

    quit(0)
