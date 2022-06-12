import pygame
from piece import Piece
from constants import WHITE_PIECE, BLACK_PIECE

class Pawn(Piece):
    def __init__(self, win, pos, color, square_size):
        super().__init__(win, pos, color, square_size)
        self.set_img('Pawn')
        self.update_available_moves()
    
    def move(self):
        if self.color == WHITE_PIECE:
            self.row -= 1
        else:
            self.row += 1
        
        return (self.row, self.col)
    
    def update_available_moves(self):
        if self.color == WHITE_PIECE:
            self.available_moves = [(self.row - 1, self.col)]
        else:
            self.available_moves = [(self.row + 1, self.col)]

