import pygame
from piece import Piece
from constants import WHITE, BLACK, ENPASSANT

class EnPassantPawn(Piece):
    def __init__(self, pos, reference_pawn, pieces_on_board):
        super().__init__(None, pos, None, None, None)
        self.reference_pawn = reference_pawn
        self.move = 0 # This is because the black pieces available moves gets updated before this en passant pawn updates its move count.
        self.type = ENPASSANT
        self.pieces_on_board = pieces_on_board
        self.killed = False
    
    def show(self, nothing):
        pass

    def move(self, new_pos):
        pass
    
    def update_available_moves(self):
        pass

    def update(self):
        if self.move == 1:
            self.kill()
        else:
            self.move += 1
    
    # Function used to remove the en passant piece 
    def kill(self):
        board = self.reference_pawn.board
        board[self.row][self.col] = None
        self.killed = True
    
    def update_threathening(self):
        pass
            

