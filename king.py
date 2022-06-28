import pygame
from piece import Piece
from constants import KING, WHITE, BLACK

class King(Piece):
    def __init__(self, win, pos, color, board, square_size):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('King')
        self.type = KING
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        self.value = 0
        self.k_castling_safe = True # If there are pieces that threathen castling
        self.q_castling_safe = True
        self.castled_rook = None
        self.castled = False
        self.king_side_free = False
        self.queen_side_free = False

        self.kingside_rook = self.board[7][7] if self.color == WHITE else self.board[0][7]
        self.queenside_rook = self.board[7][0] if self.color == WHITE else self.board[0][0]
        self.k_side_rook_square = (7, 7) if self.color == WHITE else (0, 7)
        self.q_side_rook_square = (7, 0) if self.color == WHITE else (0, 0)

        self.kingside_knight = self.board[7][6] if self.color == WHITE else self.board[0][6]
        self.queenside_knight = self.board[7][1] if self.color == WHITE else self.board[0][1]
        self.k_side_knight_square = (7, 6) if self.color == WHITE else (0, 6)
        self.q_side_knight_square = (7, 1) if self.color == WHITE else (0, 1)

        self.kingside_bishop = self.board[7][5] if self.color == WHITE else self.board[0][5]
        self.queenside_bishop = self.board[7][2] if self.color == WHITE else self.board[0][2]
        self.k_side_bishop_square = (7, 5) if self.color == WHITE else (0, 5)
        self.q_side_bishop_square = (7, 2) if self.color == WHITE else (0, 2)

        self.queen_square = (7, 3) if self.color == WHITE else (0, 3)
        self.queen = self.board[7][3] if self.color == WHITE else self.board[0][3]

        # Squares that shouldn't be treathened by any piece in order to castle
        self.k_side_castling_squares = [(7, 5), (7, 6)] if self.color == WHITE else [(0, 5), (0, 6)]
        self.q_side_castling_squares = [(7, 1), (7, 2), (7, 3)] if self.color == WHITE else [(0, 1), (0, 2), (0, 3)]
        self.k_side_castle_move = (7, 6) if self.color == WHITE else (0, 6)
        self.q_side_castle_move = (7, 2) if self.color == WHITE else (0, 2)

    
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
            rook.move((self.row, 5))
            self.castled_rook = rook

            # Move rook object in board array
            self.board[self.row][7] = None
            self.board[self.row][5] = rook
        elif col == 2:
            # Queenside castling is taking place
            rook = self.board[self.row][0]
            rook.move((self.row, 3))
            self.castled_rook = rook

            # Move rook object in board array
            self.board[self.row][0] = None
            self.board[self.row][3] = rook
        
        self.castled = True

    def undo_castle(self):
        # Undoing is easy since its just the default positions of the rook and king
        self.board[self.default_pos[0]][self.default_pos[1]] = self
        self.set_pos(self.default_pos)
        self.first_move = True

        self.board[self.castled_rook.default_pos[0]][self.castled_rook.default_pos[1]] = self.castled_rook
        self.board[self.castled_rook.row][self.castled_rook.col] = None
        self.castled_rook.set_pos(self.castled_rook.default_pos)
        self.castled_rook.first_move = True
        self.castled_rook = None
        self.castled = False
    
    # ALSO UPDATES THREATHENING VARIABLE
    def update_available_moves(self, add_to_available_moves=False):
        for move in self.moves:
            next_row = self.row + move[0]
            next_col = self.col + move[1]
            legal_move = False

            if self.valid_move(next_row, next_col):
                # Check if one of opponents pieces is in the attack move
                piece_in_attack_move = self.board[next_row][next_col]
                if piece_in_attack_move != None:
                    if piece_in_attack_move.color != self.color:
                        self.add_threathening(piece_in_attack_move)
                        legal_move = True
                else:
                    # We also want to append move if there are no pieces on the square
                    legal_move = True
            
            if legal_move:
                if add_to_available_moves:
                    self.available_moves.append((next_row, next_col))
                    # We don't need to evaluate if king is giving enemy king a check like with the other types of pieces, because he can not give check directly, only by discovered check
                else:
                    # We will add the move to possible_moves in cases where we are unsure if this move leades to the players king getting checked.
                    # Everytime we make a new move and call the set_legal_moves() function, we first add the move to possible_moves, and then check if it leades to check by using the hypothetic_move() function
                    # In the hypothetic_move() function we also call update_available_moves, but here we don't need to check further for kings getting checked, so there we just add the move directly to available_moves
                    self.possible_moves.append((next_row, next_col))

        if self.first_move:
            if self.can_castle_kingside():
                self.possible_moves.append(self.k_side_castle_move)
            
            if self.can_castle_queenside():
                self.possible_moves.append(self.q_side_castle_move)
           
    # Function that takes in a square from board and return the pieces threatening it
    # Could be added to parent Piece class, but it is only really the king that uses it
    def threathened_by(self, square):
        pieces_threathening = []
        for row in range(8):
            for piece in self.board[row]:
                if piece:
                    if piece.is_threathening(square) and piece.color != self.color:
                        pieces_threathening.append(piece)
        
        return pieces_threathening
    
    def castling_legal(self, next_col, enemy_pieces):
        legal = False

        if next_col == 6:
            # Kingside castling
            legal = self.castling_squares_safe(self.k_side_castling_squares, enemy_pieces)
            # Check to see if any of the enemy pieces are currently threathening the castling squares
        else:
            # Queenside castling
            legal = self.castling_squares_safe(self.q_side_castling_squares, enemy_pieces)
            # Check to see if any of the enemy pieces are currently threathening the castling squares
        
        return legal


        '''# Check to see if the castling squares are empty and if the rook has moved
        if next_col == 6:
            # Kingside castling
            no_knight = self.board[self.k_side_knight_square[0]][self.k_side_knight_square[1]] == None
            no_bishop = self.board[self.k_side_bishop_square[0]][self.k_side_bishop_square[1]] == None
            rook_not_moved = self.kingside_rook.first_move
            if no_knight and no_bishop and rook_not_moved:
                legal = True
        else:
            # Queenside castling
            no_knight = self.board[self.q_side_knight_square[0]][self.q_side_knight_square[1]] == None
            no_bishop = self.board[self.q_side_bishop_square[0]][self.q_side_bishop_square[1]] == None
            no_queen = self.board[self.queen_square[0]][self.queen_square[1]] == None
            rook_not_moved = self.queenside_rook.first_move
            if no_knight and no_bishop and no_queen and rook_not_moved:
                legal = True
        
        return legal'''
    
    def castling_squares_safe(self, castling_squares, enemy_pieces):
        for piece in enemy_pieces:
            # Reset and update available moves for the piece
            piece.reset_moves()
            piece.update_available_moves(add_to_available_moves=True)

            for move in piece.available_moves:
                # Check if the move is in the any of the castling squares or if the piece is putting this king in check
                if move in castling_squares or piece.check:
                    return False # Cannot castle
        
        return True
    
    # Time: 575852
    def castling_legal_2(self):
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

    def can_castle_kingside(self):
        '''rook_not_moved = False

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

        return no_knight_or_bishop and rook_not_moved'''
        # Kingside castling
        no_knight = self.board[self.k_side_knight_square[0]][self.k_side_knight_square[1]] == None
        no_bishop = self.board[self.k_side_bishop_square[0]][self.k_side_bishop_square[1]] == None
        rook_not_moved = self.kingside_rook.first_move and self.board[self.kingside_rook.row][self.kingside_rook.col] == self.kingside_rook

        return no_knight and no_bishop and rook_not_moved
    
    def can_castle_queenside(self):
        '''rook_not_moved = False

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

        return no_knight_or_bishop_or_queen and rook_not_moved'''

        # Queenside castling
        no_knight = self.board[self.q_side_knight_square[0]][self.q_side_knight_square[1]] == None
        no_bishop = self.board[self.q_side_bishop_square[0]][self.q_side_bishop_square[1]] == None
        no_queen = self.board[self.queen_square[0]][self.queen_square[1]] == None
        rook_not_moved = self.queenside_rook.first_move and self.board[self.queenside_rook.row][self.queenside_rook.col] == self.queenside_rook
        return no_knight and no_bishop and no_queen and rook_not_moved
                

