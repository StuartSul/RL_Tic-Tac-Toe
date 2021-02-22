from src.ai.ai import AI
from src.engine.board import Board
from src.gui.gui import GUI

SIZE = 3
AI_WHITE_ENABLE = True
AI_BLACK_ENABLE = False
AI_WHITE_ALGORITHM = 'reinforcement_learning'
AI_BLACK_ALGORITHM = 'random'
AI_ENABLED = AI_WHITE_ENABLE or AI_BLACK_ENABLE

def run():
    board = Board(size=SIZE)
    
    if AI_ENABLED:
        ai = AI(board)
        if AI_WHITE_ENABLE:
            ai.load(board.WHITE_TURN, AI_WHITE_ALGORITHM)
        if AI_BLACK_ENABLE:
            ai.load(board.BLACK_TURN, AI_BLACK_ALGORITHM)
        ai.start()

    GUI(board)

    if AI_ENABLED:
        ai.stop()

    quit(0)
