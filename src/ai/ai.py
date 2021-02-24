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
        self.training = False
        self.exit_flag = False
        self.board.print('Omok AI initiated')

        if Config.GUI:
            self.sleeptime = 0.1
        else:
            self.sleeptime = 0.01

        if Config.AI_WHITE_ENABLE:
            if Config.AI_WHITE_ALGORITHM not in AI_TYPES:
                self.board.print('Invalid AI type for white player; must be one of the following:', AI_TYPES)
                quit()
            if not Config.TRAIN_WHITE:
                self.threads.append(Thread(target=lambda : self.play(Board.WHITE_TURN, Config.AI_WHITE_ALGORITHM)))
                self.board.print('Omok AI loaded for white player with ' + Config.AI_WHITE_ALGORITHM + ' algorithm')
            else:
                if Config.AI_WHITE_ALGORITHM == 'random':
                    self.board.print('Cannot train a random algorithm! Exiting...')
                    quit()
                self.training = True
                self.board.print('Omok AI loaded for white player with ' + Config.AI_WHITE_ALGORITHM + ' algorithm (training mode)')

        if Config.AI_BLACK_ENABLE:
            if Config.AI_BLACK_ALGORITHM not in AI_TYPES:
                self.board.print('Invalid AI type for black player; must be one of the following:', AI_TYPES)
                quit()
            if not Config.TRAIN_BLACK:
                self.threads.append(Thread(target=lambda : self.play(Board.BLACK_TURN, Config.AI_BLACK_ALGORITHM)))
                self.board.print('Omok AI loaded for black player with ' + Config.AI_BLACK_ALGORITHM + ' algorithm')
            else:
                if Config.AI_BLACK_ALGORITHM == 'random':
                    self.board.print('Cannot train a random algorithm! Exiting...')
                    quit()
                self.training = True
                self.board.print('Omok AI loaded for black player with ' + Config.AI_BLACK_ALGORITHM + ' algorithm (training mode)')

        if self.training:
            self.threads.append(Thread(target=lambda : self.train()))

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
        if Config.GUI:
            sleep(2.0) # To prevent it from starting before GUI loads up
        while not self.exit_flag:
            if self.board.status == status_condition:
                self.board.lock.acquire()
                (i, j) = algorithm.decide_next_move()
                self.board.lock.release()
                self.board.print('AI({}) - '.format(ai_type), end='')
                self.board.place(i, j)
            else:
                sleep(self.sleeptime)
    
    def train(self):
        iter = 1
        train_white = False
        train_black = False
        if Config.AI_WHITE_ENABLE and Config.TRAIN_WHITE:
            train_white = True
            if Config.AI_WHITE_ALGORITHM == AI_TYPES[1]:
                algorithm_white = RL(self.board, Board.WHITE_TURN)
        if Config.AI_BLACK_ENABLE and Config.TRAIN_BLACK:
            train_black = True
            if Config.AI_BLACK_ALGORITHM == AI_TYPES[1]:
                algorithm_black = RL(self.board, Board.BLACK_TURN)
        if Config.GUI:
            sleep(2.0) # To prevent it from starting before GUI loads up
        elif train_white and train_black:
            self.sleeptime = 0
        while not self.exit_flag and iter < Config.TARGET_EPOCH:
            if self.board.status == Board.WHITE_TURN and train_white:
                self.board.lock.acquire()
                (i, j) = algorithm_white.decide_next_move_train()
                self.board.lock.release()
                self.board.print('AI({}) - '.format(Config.AI_WHITE_ALGORITHM), end='')
                self.board.place(i, j)
            elif self.board.status == Board.BLACK_TURN and train_black:
                self.board.lock.acquire()
                (i, j) = algorithm_black.decide_next_move_train()
                self.board.lock.release()
                self.board.print('AI({}) - '.format(Config.AI_BLACK_ALGORITHM), end='')
                self.board.place(i, j)
            elif self.board.status == Board.BLACK_WIN and train_white:
                self.board.lock.acquire()
                algorithm_white.update_policy_loss()
                self.board.lock.release()
                if iter % Config.SAVE_INTERVAL == 0:
                    algorithm_white.save_policy()
                if train_black:
                    self.board.lock.acquire()
                    algorithm_black.reset_prev_str()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_black.save_policy()
                self.board.reset()
                iter += 1
            elif self.board.status == Board.WHITE_WIN and train_black:
                self.board.lock.acquire()
                algorithm_black.update_policy_loss()
                self.board.lock.release()
                if iter % Config.SAVE_INTERVAL == 0:
                    algorithm_black.save_policy()
                if train_white:
                    self.board.lock.acquire()
                    algorithm_white.reset_prev_str()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_white.save_policy()
                self.board.reset()
                iter += 1
            elif self.board.status == Board.DRAW:
                if train_white:
                    self.board.lock.acquire()
                    algorithm_white.update_policy_loss()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_white.save_policy()
                if train_black:
                    self.board.lock.acquire()
                    algorithm_black.update_policy_loss()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_black.save_policy()
                self.board.reset()
                iter += 1
            elif self.board.status != Board.BLACK_TURN and\
                self.board.status != Board.WHITE_TURN:
                if train_white:
                    self.board.lock.acquire()
                    algorithm_white.reset_prev_str()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_white.save_policy()
                if train_black:
                    self.board.lock.acquire()
                    algorithm_black.reset_prev_str()
                    self.board.lock.release()
                    if iter % Config.SAVE_INTERVAL == 0:
                        algorithm_black.save_policy()
                self.board.reset()
                iter += 1
            else:
                sleep(self.sleeptime)
            print(iter)
