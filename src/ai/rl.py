from config import Config
from copy import deepcopy
from os import path
from random import random
from src.engine.board import Board
from src.engine.rules import Rules

class RL:
    def __init__(self, board, status_condition):
        self.board = board
        self.color = Board.BLACK_SLOT if status_condition ==\
             Board.BLACK_TURN else Board.WHITE_SLOT
        self.enemy = Board.WHITE_SLOT if status_condition ==\
             Board.BLACK_TURN else Board.BLACK_SLOT
        self.model_path = '{}{}_{}.{}'.format(
            Config.MODEL_DIRPATH, Config.MODEL_FILENAME, 'B' if self.color ==\
                Board.BLACK_SLOT else 'W', Config.MODEL_EXTENSION)
        self.board.print('Loading model from : ' + self.model_path)
        self.policy = self.initiate_policy()
        self.prev_str = None

    def initiate_policy(self):
        if not path.exists(self.model_path):
            policy = dict()
        else:
            with open(self.model_path, 'r') as model:
                policy = eval(model.read())
        return policy

    def save_policy(self):
        with open(self.model_path, 'w') as model:
            model.write(str(self.policy) + '\n')

    def evaluate(self, curr, move):
        next = deepcopy(curr)
        next[move[0]][move[1]] = self.color
        next_str = str(next)
        if next_str not in self.policy:
            if Rules.is_defeat(next, move[0], move[1]):
                self.policy[next_str] = 1
            else:
                self.policy[next_str] = 0.5
        return self.policy[next_str]
    
    def update_policy(self, curr, move):
        next = deepcopy(curr)
        next[move[0]][move[1]] = self.color
        next_str = str(next)
        if self.prev_str != None:
            self.policy[self.prev_str] +=\
                Config.LEARNING_RATE * (self.policy[next_str] -\
                    self.policy[self.prev_str])
        self.prev_str = next_str
        # self.save_policy()
    
    def update_policy_loss(self):
        if self.prev_str == None:
            return
        self.policy[self.prev_str] -= Config.LEARNING_RATE *\
            self.policy[self.prev_str]
        self.reset_prev_str()
        
    def reset_prev_str(self):
        self.save_policy()
        self.prev_str = None
 
    def decide_next_move(self):
        # evaluations : dictionary
        # key is a 2-tuple representing the next move
        # value is the value of such move
        evaluations = dict()
        curr = self.board.board

        # Evaluate all possible next moves
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                if curr[i][j] == Board.EMPTY_SLOT:
                    evaluations[(i, j)] = self.evaluate(curr, (i, j))
        
        # Sort the moves by value, in decreasing order
        moves_by_value = list(dict(reversed(sorted(
            evaluations.items(), key=lambda item: item[1]))).keys())
        
        # Pick the best move, or explore other options
        return moves_by_value[0]

    def decide_next_move_train(self):
        # evaluations : dictionary
        # key is a 2-tuple representing the next move
        # value is the value of such move
        evaluations = dict()
        curr = self.board.board

        # Evaluate all possible next moves
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                if curr[i][j] == Board.EMPTY_SLOT:
                    evaluations[(i, j)] = self.evaluate(curr, (i, j))
        self.board.print('evaluations collected : ' + str(evaluations))

        # Sort the moves by value, in decreasing order
        moves_by_value = list(dict(reversed(sorted(
            evaluations.items(), key=lambda item: item[1]))).keys())
        
        # Pick the best move, or explore other options
        if random() > Config.EXPLORATION_CHANCE:
            self.board.print('picking the best move')
            next_move = moves_by_value[0]
        else:
            self.board.print('exploring other moves')
            next_move = moves_by_value[int(random() * len(moves_by_value))]

        # Update policy and return
        self.update_policy(curr, next_move)
        return next_move
