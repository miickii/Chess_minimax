import pygame
from piece import Piece
from constants import ROOK

class Rook(Piece):
    def __init__(self, win, pos, color, board, square_size):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('Rook')
        self.type = ROOK
        self.value = 5
    
    # ALSO UPDATES THREATHENING VARIABLE
    def update_available_moves(self, add_to_available_moves=False):
        '''moves = self.check_moves_straight()
        
        self.possible_moves = moves'''
        self.update_straight_moves(add_to_available_moves)

    

