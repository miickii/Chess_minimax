import pygame
from piece import Piece
from rook import Rook
from knight import Knight
from queen import Queen
from bishop import Bishop
from en_passant_pawn import EnPassantPawn
from constants import WHITE, BLACK, PAWN, ENPASSANT, KNIGHT, BISHOP, ROOK, QUEEN, KING

class Pawn(Piece):
    def __init__(self, win, pos, color, board, square_size, en_passant_pieces):
        super().__init__(win, pos, color, board, square_size)
        self.set_img('Pawn')
        self.type = PAWN
        self.normal_move = -1 if self.color == WHITE else 1
        self.attack_moves = []
        if (self.color == WHITE):
            self.attack_moves = [(-1, -1), (-1, 1)]
        else:
            self.attack_moves = [(1, -1), (1, 1)]

        self.en_passant_pieces = en_passant_pieces
        self.en_passant_pawn = None
    
    def move(self, new_pos):
        row, col = new_pos
            
        self.row = row
        self.col = col

        # Not first move anymore
        self.first_move = False
    
    def create_en_passant(self):
        # This means that the pawn moved 2 rows
        # We want to mark the square behind the pawn it as a fianchetto oportunity
        en_passant_square = (self.row + self.normal_move, self.col) # Since the pawn hasn't moved yet, we can just use it's current position to get the square "behind"
        en_passant_pawn = EnPassantPawn(en_passant_square, self)
        self.en_passant_pawn = en_passant_pawn
        self.board[en_passant_square[0]][en_passant_square[1]] = en_passant_pawn
        
        return en_passant_pawn

        # By setting the fianchetto square equal to self, it's like having this pawn in two positions eventhough only the correct one is visible
        # This makes it easy to handle a fianchetto move
    
    def update_available_moves(self, add_to_available_moves=False):

        next_row = self.row + self.normal_move
        next_col = self.col
        
        # Check if a piece is in front of pawn, meaning that it can't pass and that the move is valid
        if self.valid_move(next_row, next_col):
            if self.board[next_row][next_col] == None:
                if add_to_available_moves:
                    self.available_moves.append((next_row, next_col))
                else:
                    self.possible_moves.append((next_row, next_col))
        
                if self.first_move:
                    # Double move on first move possible
                    next_row = self.row + self.normal_move + self.normal_move
                    if self.board[next_row][next_col] == None:
                        if add_to_available_moves:
                            self.available_moves.append((next_row, next_col))
                        else:
                            self.possible_moves.append((next_row, next_col))
        
        # Update the threathening moves
        self.update_threathening(add_to_available_moves)
    
    def update_threathening(self, add_to_available_moves):
        for move in self.attack_moves:
            next_row = self.row + move[0]
            next_col = self.col + move[1]

            # Check if move is a valid square on the board
            if self.valid_move(next_row, next_col):
                # Check if one of opponents pieces is in the attack move
                piece_in_attack_move = self.board[next_row][next_col]

                if piece_in_attack_move != None:
                    piece_color = piece_in_attack_move.color
                    if piece_in_attack_move.type == ENPASSANT:
                        piece_color = piece_in_attack_move.reference_pawn.color

                    if piece_color != self.color:
                        # If the piece is an opponent piece or the piece is an en passant piece from the opponents side
                        self.add_threathening(piece_in_attack_move)

                        if add_to_available_moves:
                            self.available_moves.append((next_row, next_col))
                            # Since this is the pawns attack move we will also evaluate if it gives check to the enemy king
                            if piece_in_attack_move.type == KING:
                                self.check = True
                        else:
                            self.possible_moves.append((next_row, next_col))
    
    def promote_pawn(self, new_piece, new_square):
        promoted_piece = new_piece
        if new_piece == KNIGHT:
            promoted_piece = Knight(self.win, new_square, self.color, self.board, self.square_size)
        elif new_piece == BISHOP:
            promoted_piece = Bishop(self.win, new_square, self.color, self.board, self.square_size)
        elif new_piece == ROOK:
            promoted_piece = Rook(self.win, new_square, self.color, self.board, self.square_size)
        elif new_piece == QUEEN:
            promoted_piece = Queen(self.win, new_square, self.color, self.board, self.square_size)

        #row, col = self.get_pos()
        #self.board[row][col] = promoted_piece
        #self.pieces_on_board.remove(self) # Remove pawn from pieces
        #promoted_piece.reset_moves()
        #promoted_piece.update_and_add_available_moves()

        return promoted_piece
            

