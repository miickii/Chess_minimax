import pygame
from piece import Piece
from constants import BISHOP

class Bishop(Piece):
    def __init__(self, win, pos, color, board, square_size):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('Bishop')
        self.type = BISHOP
        self.value = 3
    
    # ALSO UPDATES THREATHENING VARIABLE
    def update_available_moves(self, add_to_available_moves=False):
        # calculate_diag_edges() function inherited from Piece class
        start_square_right_diag, end_square_right_diag, start_square_left_diag, end_square_left_diag = self.calculate_diag_edges()

        '''# Calculate the available moves on the diag going from bottom left --> top right (right diag)
        available_right_diag = self.check_moves_diag(start_square_right_diag, end_square_right_diag, left_diag=False)

        # Calculate the available moves on the diag going from top left --> bottom right (left diag)
        available_left_diag = self.check_moves_diag(start_square_left_diag, end_square_left_diag, left_diag=True)
        
        self.possible_moves = available_right_diag + available_left_diag'''

        # Calculate the available moves on the diag going from bottom left --> top right (right diag)
        available_right_diag = self.update_diag_moves(add_to_available_moves, left_diag=False)

        # Calculate the available moves on the diag going from top left --> bottom right (left diag)
        available_left_diag = self.update_diag_moves(add_to_available_moves, left_diag=True)

