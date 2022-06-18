import pygame
from piece import Piece
from constants import QUEEN

class Queen(Piece):
    def __init__(self, win, pos, color, board, square_size):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('Queen')
        self.type = QUEEN
        self.value = 9
    
    # ALSO UPDATES THREATHENING VARIABLE
    def update_available_moves(self):
        # calculate_diag_edges() function inherited from Piece class
        start_square_right_diag, end_square_right_diag, start_square_left_diag, end_square_left_diag = self.calculate_diag_edges()

        # Calculate the available moves on the diag going from bottom left --> top right (right diag)
        available_right_diag = self.check_moves_diag(start_square_right_diag, end_square_right_diag, left_diag=False)

        # Calculate the available moves on the diag going from top left --> bottom right (left diag)
        available_left_diag = self.check_moves_diag(start_square_left_diag, end_square_left_diag, left_diag=True)

        # Calculate the available horizontal and vertical moves
        available_straight = self.check_moves_straight()
        
        self.possible_moves = available_right_diag + available_left_diag + available_straight
    
    def update_available_moves_2(self, board=None):
        # calculate_diag_edges() function inherited from Piece class
        start_square_right_diag, end_square_right_diag, start_square_left_diag, end_square_left_diag = self.calculate_diag_edges()

        # Calculate the available moves on the diag going from bottom left --> top right (right diag)
        available_right_diag = self.check_moves_diag_2(start_square_right_diag, end_square_right_diag, board=board, left_diag=False)

        # Calculate the available moves on the diag going from top left --> bottom right (left diag)
        available_left_diag = self.check_moves_diag_2(start_square_left_diag, end_square_left_diag, board=board, left_diag=True)

        # Calculate the available horizontal and vertical moves
        available_straight = self.check_moves_straight_2(board=board)
        
        return available_right_diag + available_left_diag + available_straight

