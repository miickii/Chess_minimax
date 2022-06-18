import pygame
from piece import Piece
from constants import KING, WHITE, BLACK

class King(Piece):
    def __init__(self, win, pos, color, board, square_size, pieces_on_board):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('King')
        self.type = KING
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        self.value = 999
        self.k_castling_safe = True # If there are pieces that threathen castling
        self.q_castling_safe = True

        self.pieces_on_board = pieces_on_board
    
    def move(self, new_pos):
        row, col = new_pos

        self.row = row
        self.col = col

        # Not first move anymore
        self.first_move = False
    
    def castle(self, col):
        # We also want to move the rook depending on castle side and player side
        if col == 6:
            # Kingside castling is taking place
            rook = self.board[self.row][7]
            if rook != None:
                rook.move((self.row, 5))

            # Move rook object in board array
            self.board[self.row][7] = None
            self.board[self.row][5] = rook
        elif col == 2:
            # Queenside castling is taking place
            rook = self.board[self.row][0]
            if rook != None:
                rook.move((self.row, 3))

            # Move rook object in board array
            self.board[self.row][0] = None
            self.board[self.row][3] = rook
    
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
        
        if self.first_move:
            if self.can_castle_kingside() and self.k_castling_safe:
                if self.color == WHITE:
                    # Checking if f1 and g1 squares are threathened by any pieces which would hinder castling
                    f1_safe = len(self.threathened_by((7, 5))) < 1
                    g1_safe = len(self.threathened_by((7, 6))) < 1

                    if f1_safe and g1_safe:
                        self.possible_moves.append((7, 6))
                else:
                    # Checking if f8 and g8 squares are threathened by any pieces which would hinder castling
                    f8_safe = len(self.threathened_by((0, 5))) < 1
                    g8_safe = len(self.threathened_by((0, 6))) < 1

                    if f8_safe and g8_safe:
                        self.possible_moves.append((0, 6))
            elif self.k_castling_safe == False:
                self.k_castling_safe = True

            if self.can_castle_queenside() and self.q_castling_safe:
                if self.color == WHITE:
                    # Checking if b1, c1 and d1 squares are threathened by any pieces which would hinder castling
                    b1_safe = len(self.threathened_by((7, 1))) < 1
                    c1_safe = len(self.threathened_by((7, 2))) < 1
                    d1_safe = len(self.threathened_by((7, 3))) < 1

                    if b1_safe and c1_safe and d1_safe:
                        self.possible_moves.append((7, 2))
                else:
                    # Checking if b8, c8 and d8 squares are threathened by any pieces which would hinder castling
                    b8_safe = len(self.threathened_by((0, 1))) < 1
                    c8_safe = len(self.threathened_by((0, 2))) < 1
                    d8_safe = len(self.threathened_by((0, 3))) < 1

                    if b8_safe and c8_safe and d8_safe:
                        self.possible_moves.append((0, 2))
            elif self.q_castling_safe == False:
                self.q_castling_safe = True
    
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
           
    # Function that takes in a square from board and return the pieces threatening it
    # Could be added to parent Piece class, but it is only really the king that uses it
    def threathened_by(self, square):
        pieces_threathening = []
        for piece in self.pieces_on_board:
            if piece.is_threathening(square) and piece.color != self.color:
                pieces_threathening.append(piece)
        
        return pieces_threathening

    def can_castle_kingside(self):
        rook_not_moved = False

        if self.color == WHITE:
            no_knight_or_bishop = self.board[7][5] == None and self.board[7][6] == None
            kingside_rook = self.board[7][7]
            if kingside_rook != None:
                rook_not_moved = kingside_rook.first_move
        else:
            no_knight_or_bishop = self.board[0][5] == None and self.board[0][6] == None
            kingside_rook = self.board[0][7]
            if kingside_rook != None:
                rook_not_moved = kingside_rook.first_move

        return no_knight_or_bishop and rook_not_moved
    
    def can_castle_queenside(self):
        rook_not_moved = False

        if self.color == WHITE:
            no_knight_or_bishop_or_queen = self.board[7][1] == None and self.board[7][2] == None and self.board[7][3] == None
            queenside_rook = self.board[7][0]
            if queenside_rook != None:
                rook_not_moved = queenside_rook.first_move
        else:
            no_knight_or_bishop_or_queen = self.board[0][1] == None and self.board[0][2] == None and self.board[0][3] == None
            queenside_rook = self.board[0][0]
            if queenside_rook != None:
                rook_not_moved = queenside_rook.first_move
            king_not_moved = self.board[0][4].first_move

        return no_knight_or_bishop_or_queen and rook_not_moved
                

