from src.ai.random import Random
from src.ai.rl import RL
from src.engine.board import Board
from threading import Thread
from time import sleep

AI_TYPES = ['random', 'reinforcement_learning']

class AI:
    """Omok AI Runner"""
    def __init__(self, board):
        self.board = board
        self.threads = []
        self.exit_flag = False
        self.board.print('Omok AI initiated')

    def load(self, status_condition, ai_type):
        if len(self.threads) >= 2:
            self.board.print('No more AI threads can be created')
        elif status_condition != Board.BLACK_TURN and status_condition != Board.WHITE_TURN:
            self.board.print('Invalid status condition for AI')
        elif len(self.threads) == 1 and status_condition == self.threads[0][1]:
            self.board.print('Cannot create duplicate AI threads with the same status condition')
        elif ai_type not in AI_TYPES:
            self.board.print('Invalid AI type; must be one of following:', AI_TYPES)
        else:
            self.threads.append((Thread(target=lambda : self.play(status_condition, ai_type)), status_condition))
            self.board.print('Omok AI loaded with condition ' + str(status_condition) + ' and ' + ai_type + ' algorithm')
    
    def start(self):
        self.exit_flag = False
        for thread in self.threads:
            thread[0].start()
        self.board.print('Omok AI started')

    def stop(self):
        self.exit_flag = True
        for thread in self.threads:
            thread[0].join()
        self.board.print('Omok AI stopped')

    def play(self, status_condition, ai_type):
        if ai_type == 'random':
            algorithm = Random(self.board)
        elif ai_type == 'reinforcement_learning':
            algorithm = RL(self.board, status_condition)
        sleep(2.0) # To prevent it from starting before GUI loads up
        while not self.exit_flag:
            if self.board.status == status_condition:
                self.board.lock.acquire()
                (i, j) = algorithm.decide_next_move()
                self.board.lock.release()
                self.board.print('AI({}) - '.format(ai_type), end='')
                self.board.place(i, j)
            else:
                sleep(0.1)