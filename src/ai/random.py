from src.engine.board import Board
from random import random

class Random:
    def __init__(self, board):
        self.board = board

    def decide_next_move(self):
        board = self.board.board
        num_empty_slots = 0

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Board.EMPTY_SLOT:
                    num_empty_slots += 1

        next_move = int(random() * num_empty_slots)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Board.EMPTY_SLOT:
                    num_empty_slots -= 1
                    if num_empty_slots == next_move:
                        return i, j

        return 0, 0 # This should never happen