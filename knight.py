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
    def update_available_moves(self, add_to_available_moves=False):
        for move in self.moves:
            next_row = self.row + move[0]
            next_col = self.col + move[1]

            if self.valid_move(next_row, next_col):
                # Check if one of opponents pieces is in the attack move
                piece_in_attack_move = self.board[next_row][next_col]
                if piece_in_attack_move != None:
                    if piece_in_attack_move.color != self.color:
                        self.add_threathening(piece_in_attack_move)
                        legal_move = True

                        if add_to_available_moves:
                            self.available_moves.append((next_row, next_col))
                            # We will also check if this move puts enemy king in check
                            if piece_in_attack_move.type == KING:
                                self.check = True
                        else:
                            self.possible_moves.append((next_row, next_col))
                else:
                    # We also want to append move if there are no pieces on the square
                    if add_to_available_moves:
                        self.available_moves.append((next_row, next_col))
                    else:
                        self.possible_moves.append((next_row, next_col))

