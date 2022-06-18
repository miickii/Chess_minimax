import pygame
from piece import Piece
from constants import KNIGHT, WHITE, BLACK, KING

class Knight(Piece):
    def __init__(self, win, pos, color, board, square_size):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('Knight')
        self.type = KNIGHT
        self.moves = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        self.value = 3
    
    # ALSO UPDATES THREATHENING VARIABLE
    def update_available_moves(self):
        next_row = None
        next_col = None
        for move in self.moves:
            next_row = self.row + move[0]
            next_col = self.col + move[1]

            if self.valid_move(next_row, next_col):
                # Check if one of opponents pieces is in the attack move
                piece_in_attack_move = self.board[next_row][next_col]
                if piece_in_attack_move != None:
                    if piece_in_attack_move.color != self.color:
                        self.add_threathening(piece_in_attack_move)
                        self.possible_moves.append((next_row, next_col))
                else:
                    # We also want to append move if there are no pieces on the square
                    self.possible_moves.append((next_row, next_col))
    
    def update_available_moves_2(self, board=None):
        next_row = None
        next_col = None
        moves = []
        for move in self.moves:
            next_row = self.row + move[0]
            next_col = self.col + move[1]

            if self.valid_move(next_row, next_col):
                # Check if one of opponents pieces is in the attack move
                piece_in_attack_move = board[next_row][next_col]
                if piece_in_attack_move != None:
                    piece_color = WHITE if piece_in_attack_move > 0 else BLACK
                    if piece_color != self.color:
                        moves.append((next_row, next_col))
                        if abs(piece_in_attack_move) == KING:
                            self.check = True
                else:
                    # We also want to append move if there are no pieces on the square
                    moves.append((next_row, next_col))
        
        return moves

