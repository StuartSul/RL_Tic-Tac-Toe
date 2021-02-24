from config import Config
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

        if Config.AI_WHITE_ENABLE:
            if Config.AI_WHITE_ALGORITHM not in AI_TYPES:
                self.board.print('Invalid AI type for white player; must be one of the following:', AI_TYPES)
                quit()
            if not Config.TRAIN_WHITE:
                self.threads.append(Thread(target=lambda : self.play(Board.WHITE_TURN, Config.AI_WHITE_ALGORITHM)))
                self.board.print('Omok AI loaded for white player with ' + Config.AI_WHITE_ALGORITHM + ' algorithm')
            else:
                self.threads.append(Thread(target=lambda : self.train(Board.WHITE_TURN, Config.AI_WHITE_ALGORITHM)))
                self.board.print('Omok AI loaded for white player with ' + Config.AI_WHITE_ALGORITHM + ' algorithm (training mode)')

        if Config.AI_BLACK_ENABLE:
            if Config.AI_BLACK_ALGORITHM not in AI_TYPES:
                self.board.print('Invalid AI type for black player; must be one of the following:', AI_TYPES)
                quit()
            if not Config.TRAIN_BLACK:
                self.threads.append(Thread(target=lambda : self.play(Board.BLACK_TURN, Config.AI_BLACK_ALGORITHM)))
                self.board.print('Omok AI loaded for black player with ' + Config.AI_BLACK_ALGORITHM + ' algorithm')
            else:
                self.threads.append(Thread(target=lambda : self.train(Board.BLACK_TURN, Config.AI_BLACK_ALGORITHM)))
                self.board.print('Omok AI loaded for black player with ' + Config.AI_BLACK_ALGORITHM + ' algorithm (training mode)')

        self.exit_flag = False
        for thread in self.threads:
            thread.start()
        self.board.print('Omok AI started')

    def stop(self):
        self.exit_flag = True
        for thread in self.threads:
            thread.join()
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
    
    def train(self, status_condition, ai_type):
        if ai_type == 'random':
            print('Cannot train random AI! Exiting...')
            quit(0)
        elif ai_type == 'reinforcement_learning':
            algorithm = RL(self.board, status_condition)
        sleep(2.0) # To prevent it from starting before GUI loads up
        while not self.exit_flag:
            if self.board.status == status_condition:
                self.board.lock.acquire()
                (i, j) = algorithm.decide_next_move_train()
                self.board.lock.release()
                self.board.print('AI({}) - '.format(ai_type), end='')
                self.board.place(i, j)
            elif (self.board.status == Board.BLACK_WIN and\
                status_condition == Board.WHITE_TURN) or\
                    (self.board.status == Board.WHITE_WIN and\
                        status_condition == Board.BLACK_TURN) or\
                            self.board.status == Board.DRAW:
                            self.board.lock.acquire()
                            algorithm.update_policy_loss()
                            self.board.lock.release()
                            self.board.reset()
            elif self.board.status != Board.BLACK_TURN and\
                self.board.status != Board.WHITE_TURN:
                    self.board.lock.acquire()
                    algorithm.reset_prev_str()
                    self.board.lock.release()
                    self.board.reset()
            else:
                sleep(0.1)
