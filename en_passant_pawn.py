import pygame
from piece import Piece
from constants import WHITE, BLACK, ENPASSANT

class EnPassantPawn(Piece):
    def __init__(self, pos, reference_pawn):
        super().__init__(None, pos, None, None, None)
        self.move_count = 1 # This is because the black pieces available moves gets updated before this en passant pawn updates its move count.
        self.type = ENPASSANT
        self.reference_pawn = reference_pawn
        self.killed = False
    
    def show(self, nothing):
        pass

    def move(self, new_pos):
        pass
    
    def update_available_moves(self, add_to_available_moves=None):
        pass

    def update(self):
        if self.move_count == 1:
            self.kill()
        
        self.move_count += 1
    
    # Function used to remove the en passant piece 
    # Not used because we can do everything from move_piece function in board.py
    def kill(self):
        board = self.reference_pawn.board
        board[self.row][self.col] = None
        self.killed = True
        self.reference_pawn.en_passant_pawn = None
    
    def update_threathening(self):
        pass
            

