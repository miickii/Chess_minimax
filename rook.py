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
    def update_available_moves(self):
        moves = self.check_moves_straight()
        
        self.possible_moves = moves
    
    def update_available_moves_2(self, board=None):
        moves = self.check_moves_straight_2(board=board)
        
        return moves

    

