from src.engine.rules import Rules
from src.engine.traces import Traces
from threading import Lock

class Board:
    """Tic-tac-toe game board engine"""
    EMPTY_SLOT = '-' # These three variables must be single character
    BLACK_SLOT = 'B'
    WHITE_SLOT = 'W'

    BLACK_TURN = 10
    BLACK_WIN = 11
    WHITE_TURN = 20
    WHITE_WIN = 21
    DRAW = 30

    INVALID_CALL = 40
    INIT_STATUS = BLACK_TURN

    def __init__(self, size=3, silent=False):
        if size < 3:
            raise ValueError('Board size must be greater than or equal to 3x3')
        self.size = size
        self.silent = silent # if True, blocks all CLI messages
        self.board = None
        self.empty_slots = None
        self.traces = None
        self.status = None
        self.gui = None
        self.lock = Lock()
        self.reset()
        self.print('Board engine loaded')

    def __str__(self):
        board_str  = '\nBoard Status: ' + str(self.status)
        board_str += '\nGUI: ' + str(self.gui)
        board_str += '\nSilence Mode: ' + str(self.silent)
        board_str += '\nCurrent State:'
        board_str += self.__repr__()
        return board_str

    def __repr__(self):
        board_repr = '\n'
        for i in range (self.size):
            for j in range(self.size):
                board_repr += self.board[i][j]
            board_repr += '\n'
        board_repr += '\n'
        return board_repr

    def reset(self):
        if not self.lock.acquire(False):
            self.print('Board engine is currently locked')
            return
        self.board = []
        self.empty_slots = set()
        for i in range (self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(Board.EMPTY_SLOT)
                self.empty_slots.add((i, j))
        self.traces = Traces()
        self.status = Board.INIT_STATUS
        self.clear_gui()
        self.print('Board has been reset')
        self.lock.release()

    def place(self, i, j):
        if not self.lock.acquire(False):
            self.print('Board engine is currently locked')
            return Board.INVALID_CALL
        if not self.is_valid_slot(i, j):
            self.lock.release()
            return Board.INVALID_CALL

        self.board[i][j] = Board.BLACK_SLOT if (self.status == Board.BLACK_TURN) else Board.WHITE_SLOT
        self.empty_slots.remove((i, j))
        self.traces.push(self.board[i][j], i, j)
        self.print(self.traces.format_trace(self.traces.size(), self.traces.peek()))

        if Rules.is_defeat(self.board, i, j):
            if self.status == Board.BLACK_TURN:
                self.print('Game over: black wins!')
                self.status = Board.BLACK_WIN
            elif self.status == Board.WHITE_TURN:
                self.print('Game over: white wins!')
                self.status = Board.WHITE_WIN
        elif len(self.empty_slots) == 0:
            self.print('Game over: draw!')
            self.status = Board.DRAW
        else:
            self.status = Board.BLACK_TURN if (self.status == Board.WHITE_TURN) else Board.WHITE_TURN

        self.update_gui(i, j)
        self.lock.release()
        return self.status
    
    def is_valid_slot(self, i, j):
        if self.status == Board.BLACK_WIN or self.status == Board.WHITE_WIN:
            self.print('Game over: ' + ('black' if (self.status == Board.BLACK_WIN) else 'white') + ' wins!')
            return False
        elif self.status == Board.DRAW:
            self.print('Game over: draw!')
            return False
        elif i < 0 or j < 0 or i >= self.size or j >= self.size:
            self.print('Cannot place piece outside the board range: ({}, {})'.format(i, j))
            return False
        elif self.board[i][j] != Board.EMPTY_SLOT:
            self.print('Cannot place piece on a non-empty spot: ({}, {}) already placed with {}'.format(i, j, self.board[i][j]))
            return False
        elif Rules.is_three(self.board, i, j):
            self.print('Cannot place piece on a spot that creates three by three condition')
            return False
        elif self.status == Board.BLACK_TURN or self.status == Board.WHITE_TURN:
            return True
        else:
            self.print('Invalid status code {}'.format(self.status))
            return False

    def load_gui(self, gui):
        self.gui = gui
        self.print('GUI successfully loaded to game engine')

    def update_gui(self, i, j):
        if self.gui != None:
            self.gui.update(i=i, j=j)

    def clear_gui(self):
        if self.gui != None:
            self.gui.update()

    def print(self, message, end='\n'):
        if not self.silent:
            print(message, end=end)
