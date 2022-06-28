from piece import Piece
import pygame
import random
from box import Box
from king import King
from rook import Rook
from knight import Knight
from queen import Queen
from pawn import Pawn
from bishop import Bishop
from constants import *

class Board():
    def __init__(self, win, pos, board_size, game_state):
        self.win = win
        self.pos = pos
        self.x = int(self.pos[0])
        self.y = int(self.pos[1])
        self.width = board_size[0]
        self.height = board_size[1]
        self.rows, self.cols = 8, 8
        self.grid = []
        # Filling board with None
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(None)
        
        self.grid_2 = []
        # Filling board with None
        for i in range(self.rows):
            self.grid_2.append([])
            for j in range(self.cols):
                self.grid_2[i].append(None)

        self.square_size = self.width / 8
        self.highlighted_squares = []
        self.highlighted_moves = []
        self.squares = [] # 2d array of surfaces for each square on board
        for i in range(self.rows):
            self.squares.append([])
            for j in range(self.cols):
                square = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                square.fill(C_TRANSPARENT_GREEN)
                self.squares[i].append(square)

        self.img = pygame.image.load('assets/extras/board3_2.png')
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.black_piece_imgs = []
        self.white_piece_imgs = []
        self.piece_img_size = (41, 82) # Hard coded but easy to find
        self.grey_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.grey_overlay.fill(C_GREY_TRANSPARENT)

        # TEXT
        self.board_font = pygame.font.Font('freesansbold.ttf', 32)

        # COORDINATES AND POSITIONS FOR PROMOTION PIECE SELECTION BOX
        margin_between_imgs = self.piece_img_size[0]
        box_height = self.square_size * 2
        box_width = self.piece_img_size[0] * 5 + margin_between_imgs * 6
        box_x = self.pos[0] + (self.width / 2) - (box_width / 2)
        box_y = self.pos[1] + (self.height / 2) - (box_height / 2)
        promotion_img_positions = [] # Index 0 = pawn, 1 = knight, 2 = bishop, 3 = rook, 4 = queen
        promotion_img_sizes = [self.piece_img_size for i in range(5)] # Just the same size 5 times. We do this because it's convenient for the Box class
        start_img_x = box_x + margin_between_imgs
        for i in range(5):
            img_x = self.piece_img_size[0] * i + margin_between_imgs * i + start_img_x
            img_y = box_y + (box_height / 2) - (self.piece_img_size[1] / 2)
            promotion_img_positions.append((img_x, img_y))
        
        self.promotion_box = Box(self.win, C_GREY, (box_x, box_y), box_width, box_height, img_positions=promotion_img_positions, img_sizes=promotion_img_sizes)

        # COORDINATES AND POSITIONS FOR PROMOTION ENDING BOX
        box_height = self.height / 4
        box_width = self.width / 2
        box_x = self.pos[0] + (self.width / 2) - (box_width / 2)
        box_y = self.pos[1] + (self.height / 2) - (box_height / 2)
        # Checkmate text
        self.checkmate_text = self.board_font.render('CHECKMATE', True, C_RED)
        self.checkmate_text_rect = self.checkmate_text.get_rect()
        # set the center of the rectangular object.
        self.checkmate_text_rect.center = (box_x + box_width / 2, box_y + box_height / 3)

        # Stalemate text
        self.stalemate_text = self.board_font.render('STALEMATE', True, C_BLUE)
        self.stalemate_text_rect = self.stalemate_text.get_rect()
        # set the center of the rectangular object.
        self.stalemate_text_rect.center = (box_x + box_width / 2, box_y + box_height / 2)

        # White won text
        self.white_won_text = self.board_font.render('White Won', True, C_WHITE)
        self.white_won_text_rect = self.white_won_text.get_rect()
        # set the center of the rectangular object.
        self.white_won_text_rect.center = (box_x + box_width / 2, box_y + box_height / 1.5)

        # Black won text
        self.black_won_text = self.board_font.render('Black Won', True, C_BLACK)
        self.black_won_text_rect = self.black_won_text.get_rect()
        # set the center of the rectangular object.
        self.black_won_text_rect.center = (box_x + box_width / 2, box_y + box_height / 1.5)
        
        # We will add imgs and img_positions when game ends where we know the result of game
        self.end_box = Box(self.win, C_GREY, (box_x, box_y), box_width, box_height, imgs=[], img_positions=[])

        self.game_state = game_state
        self.turn_based = None
        self.highlight = None
        self.config_game_state()

        self.white_player = None
        self.black_player = None
        self.player_turn = WHITE
        self.next_player = BLACK
        self.black_king = None
        self.white_king = None
        self.black_score = 39
        self.white_score = 39

        self.num_of_moves = 1 # The total amount of moves, where black and white moves are independent
        self.curr_move = 1
        self.white_captured = []
        self.black_captured = []
        self.check = False
        self.checking_pieces = []
        self.checked_king = None
        self.stalemate, self.checkmate = 0, 1
        self.result = None

        self.selection_state, self.move_state, self.promotion_state, self.ended_state = 0, 1, 2, 3
        self.board_state = self.selection_state

        self.selected_piece = None
        self.promotion_pawn = None
        self.promotion_color = None

        self.pieces_on_board = []
        self.white_pieces_on_board = []
        self.black_pieces_on_board = []
        self.en_passant_pieces = []

        # COPIES
        '''self.grid = None
        self.black_player.score = None
        self.white_player.score = None
        self.black_captured = None
        self.white_captured = None
        self.white_pieces_on_board = None
        self.black_pieces_on_board = None
        self.pieces_on_board = None'''

        self.init_pieces()
    
    def show(self):
        self.win.blit(self.img, self.pos)

        '''for row in range(self.rows):
            for piece in self.grid[row]:
                if piece: # Square in grid is not None, but a Piece object
                    piece.show(self.y)'''
        
        for arr in self.highlighted_moves:
            square = arr[0]
            pos = arr[1]
            # The pos is in the form of column and row, so it has to be scaled by the square_size
            x = pos[1] * self.square_size # The column position
            y = pos[0] * self.square_size + self.y # The row position (also taking into account the y position of board on screen)
            self.win.blit(square, (x, y))
        
        for piece in self.pieces_on_board:
            piece.show(self.y)
        
        if self.board_state == self.promotion_state:
            self.win.blit(self.grey_overlay, self.pos)
            self.promotion_box.draw()
           
            if self.promotion_color == WHITE:
                imgs = self.white_piece_imgs
            else:
                imgs = self.black_piece_imgs
            
            for i, img in enumerate(imgs):
                img_x, img_y = self.promotion_box.img_positions[i]
                self.win.blit(img, (img_x, img_y))
        elif self.board_state == self.ended_state:
            self.win.blit(self.grey_overlay, self.pos)
            self.end_box.draw()

        # Render captured pieces
        x_offset = 10
        for piece in self.white_captured:
            self.win.blit(piece.img, (x_offset, self.y + self.height + 10))
            x_offset += piece.img_size[0] + 15
        x_offset = 10
        for piece in self.black_captured:
            self.win.blit(piece.img, (x_offset, 10))
            x_offset += piece.img_size[0] + 15
    
    def run(self):
        pass

    
    def mouse_clicked(self, pos):
        #HANDLE ALL OF THIS IN SEPARATE FUNCTIONS THAT GETS CALLED IN THE MAIN LOOP

        # Get the square clicked on
        clicked_square = self.get_square(pos)

        if self.board_state == self.move_state:
            new_square = None
            # Check if the clicked_square is any of the squares in highlighted_squares
            for square in self.highlighted_moves:
                square_pos = square[1]
                if square_pos == clicked_square:
                    # Meaning that the move is among one of the available moves
                    # If that's the case we want to set the new_move to this square
                    new_square = clicked_square
                    break # After making a move the rest of the highlighted squares/possible moves doesn't need to be checked
            
            if new_square:
                self.move_piece(self.selected_piece, new_square)
            else:
                # If the player doesn't click a valid square for the piece it means that they either deselected the piece or chose another piece.
                # In that case, the move_state will still be true as the move_piece() function hasn't been called
                # move_state should be False and we want to check if the player clicked another piece instead
                self.board_state = self.move_state
                self.update_selected_piece(clicked_square)
        elif self.board_state == self.promotion_state:
            x, y = pos
            promotion_square = self.promotion_pawn.get_pos()
            new_piece = None
            
            img_clicked = self.promotion_box.clicked_img(pos)
            # 0 = pawn, 1 = knight, 2 = bishop, 3 = rook, 4 = queen
            if img_clicked == 1:
                new_piece = KNIGHTK
            elif img_clicked == 2:
                new_piece = BISHOP
            elif img_clicked == 3:
                new_piece = ROOK
            elif img_clicked == 4:
                new_piece = QUEEN

            if new_piece != None: # If the piece is None, that means that promotion piece is a pawn, and in that case we don't need to change the piece
                new_piece = self.promotion_pawn.promote_pawn(new_piece)
                self.pieces_on_board.remove(self.promotion_pawn) # Remove pawn from pieces
                self.pieces_on_board.append(new_piece)

                if self.player_turn == WHITE:
                    self.white_pieces_on_board.append(new_piece)
                else:
                    self.black_pieces_on_board.append(new_piece)
            else:
                new_piece = self.promotion_pawn
            
            # We move the piece even though it is in the same position, to check for check and update next players move with this piece taken into account
            self.move_piece(new_piece, promotion_square)
            
            # This is already done in move_piece
            '''
            self.board_state = self.selection_state # Player have selected what piece to promote and we have to change state to selection again
            self.switch_turn()'''

        elif self.board_state == self.selection_state: # Not in move state or promotion state. In that case we want to check if player selected a piece that should be highlighted
            self.update_selected_piece(clicked_square)
        elif self.board_state == self.ended_state:
            # ADD OPTION FOR PLAY AGAIN, ANALYZE??, SEE BOARD
            pass

     # Function to check if the player has clicked a piece on the board. If so, we want to highlight available moves and check if it's the correct player
    def update_selected_piece(self, square):
        # Stop rendering any current highlighted squares
        self.highlighted_moves = []
        self.selected_piece = self.get_piece(square)
        if self.selected_piece != None: # Player clicked on a piece
            if not self.turn_based:
                self.player_turn = self.selected_piece.color

            if self.selected_piece.color == self.player_turn:
                # Highligt available moves
                self.highlight_moves(self.selected_piece.available_moves, self.selected_piece.threathening)
                self.board_state = self.move_state # A piece is selected and we can now move it, so we set board state to move
    
    def highlight_moves(self, available_moves, threathened_pieces):
        for pos in available_moves:
            row, col = pos
            square = self.squares[row][col] # Retrieve the square corresponding to the position
            square.fill(C_TRANSPARENT_GREEN)

            # Check the square contains a piece that is being threathened
            for piece in threathened_pieces:
                if piece.get_pos() == pos:
                    # If the square contains a threathened piece, we will highlight that square with red
                    square.fill(C_TRANSPARENT_RED)

            self.highlighted_moves.append([square, pos])  # Adding that square to the current highlighted squares, so it will be rendered to the window. We also add the position for when it get's blittet to the screen
    
    def move_piece_2(self, piece_obj, new_square):
        # We want to reset checking pieces and check every move, because if a move was made that means that player avoided check if he was in check
        self.check = False
        self.checking_pieces = []
        # CODE FOR MOVING THE PIECE
        curr_row, curr_col = piece_obj.get_pos()
        new_row, new_col = new_square

        # Move piece in grid variable and update captured pieces
        piece = self.grid_2[curr_row][curr_col]
        self.grid_2[curr_row][curr_col] = None 
        piece_at_new_square = self.grid_2[new_row][new_col]

        # Handle a case of en passant
        if piece_at_new_square and abs(piece_at_new_square) == ENPASSANT:
            if abs(piece) != PAWN:
                # If the piece is an en passant piece, other type of pieces besides pawns should just ignore it
                piece_at_new_square = None
            else:
                if player_turn == WHITE:
                    # If it was a white en passant pawn the pawn is above it one row
                    piece_at_new_square = self.grid_2[new_row-1][new_col]
                    self.grid_2[new_row-1][new_col] = None
                else:
                    # If black it is below 1 row
                    piece_at_new_square = self.grid_2[new_row+1][new_col]
                    self.grid_2[new_row+1][new_col] = None

        '''if piece_at_new_square:
            # Check to see if is a black or white piece
            if piece_at_new_square.color == WHITE: # Black captured a piece
                self.black_player.score += piece_at_new_square.value
                self.white_player.enemy_score += piece_at_new_square.value

                self.black_captured.append(piece_at_new_square)
                self.white_pieces_on_board.remove(piece_at_new_square)
            else: # White captured
                self.white_player.score += piece_at_new_square.value
                self.black_player.enemy_score += piece_at_new_square.value

                self.white_captured.append(piece_at_new_square)
                self.black_pieces_on_board.remove(piece_at_new_square)'''
            
            # Remove piece from pieces_on_board array
            #self.pieces_on_board.remove(piece_at_new_square)

        # Move piece in grid array to the new position
        self.grid_2[new_row][new_col] = piece
        piece_obj.set_pos((new_row, new_col))

        # If the moved piece was a pawn and it moved to the final rank, we want to activate the promotion state
        
        end_rank = True if (self.player_turn == WHITE and new_row == 0) or (self.player_turn == BLACK and new_row == 7) else False
        if abs(piece) == PAWN and end_rank:
            self.grid_2[new_row][new_col] = QUEEN
        
        # This is to make sure that every en passant pawn gets removed after each move
        for i in range(len(self.en_passant_pieces)-1, -1, -1):
            pawn = self.en_passant_pieces[i]
            pawn.update()
        
        # Determine all legal moves for next player
        self.calculate_legal_moves_2((new_row, new_col))
        legal_moves_count = len(self.legal_moves)

        self.switch_turn()
        return self.grid_2

    def evaluate_board(self):
        pass
    
    def make_move(self, move):
        possible_pieces = ['N', 'B', 'R', 'Q', 'K']
        move = move.replace("+", "").replace("#", "")
        move_piece = "" # p = pawn, r = rook, b = bishop, k = knight, q = queen, K = king
        square = ""
        curr_file = ""
        curr_rank = ""
        promotion_piece = ""
        
        if move[0] not in possible_pieces:
            # Pawn move or castling
            if move == "O-O-O":
                # Queenside castling
                move_piece = "K"
                square = "c1" if self.player_turn == WHITE else "c8"
            elif move == "O-O":
                # Kingside castling
                move_piece = "K"
                square = "g1" if self.player_turn == WHITE else "g8"
            else:
                # Pawn move
                if "x" in move:
                    curr_file, square = move.split("x")
                elif "=" in move:
                    # Pawn promoted
                    square, promotion_piece = move.split("=")
                else:
                    square = move
                move_piece = "P"
        else:
            # Any other move
            move = move.replace("x", "") # We remove the x indicating takes because it's distracting and redundant information
            move_piece = move[0]
            if len(move) == 4:
                # Means that piece is either rook or knight, and there are two of them that can make that move
                square = move[2::]
                if move[1].isdigit():
                    curr_rank = move[1]
                else:
                    curr_file = move[1]
            else:
                square = move[1::]
        
        # Turn square into move cordinates
        square = BOARD_POSITIONS[square]

        # Find the piece in question by looping through players pieces and check type and wether or not the move square is in the piece's available_moves
        curr_pieces = self.white_pieces_on_board if self.player_turn == WHITE else self.black_pieces_on_board
        piece_possibilities = [] # Will mostly only contain one value. But in the case that the piece is a rook or knight, and both of them can make the same move, then this array will have 2 values
        for piece in curr_pieces:
            if (piece.type == PAWN and move_piece == "P") or (piece.type == KNIGHT and move_piece == "N") or (piece.type == BISHOP and move_piece == "B") or (piece.type == ROOK and move_piece == "R") or (piece.type == QUEEN and move_piece == "Q") or (piece.type == KING and move_piece == "K"):
                # Means that it's the correct piece type
                if square in piece.available_moves:
                    piece_possibilities.append(piece)
        
        piece = None # The Piece object that is being moved
        for possibility in piece_possibilities:
            if curr_file != "":
                if possibility.col == FILE_TO_COL[curr_file]:
                    piece = possibility
            elif curr_rank != "":
                if possibility.row == RANK_TO_ROW[curr_rank]:
                    piece = possibility
            else:
                # The case if there is only one possible piece that can make this move
                piece = possibility
        
        # Now we can finally make the move on board
        self.move_piece(piece, square)
    
    # Previous functions to calculate checkmate
    def calculate_checkmate(self):
        self.checked_king = self.white_king if self.player_turn == BLACK else self.black_king # Color of player that made current move caused check
        total_legal_moves = 0

        for piece in self.pieces_on_board:
            if piece.color == self.checked_king.color:
                # If it's of the pieces from the player in check
                moves = self.legal_moves_in_check(piece)
                total_legal_moves += len(moves)
                piece.available_moves = moves
        
        if total_legal_moves == 0:
            print("CHECKMATE!")
            self.result = self.checkmate
            self.handle_game_finished()
    
    def legal_moves_in_check(self, piece):
        moves = []
        for checking_piece in self.checking_pieces:
            # Looping through all the pieces that are giving check
            for move in piece.available_moves:
                # Looping through each move of a given piece from player in check to check if it can stop it
                if move == checking_piece.get_pos():
                    moves.append(move)
                else:
                    still_check = self.hypothetic_move(piece, [checking_piece], move, self.checked_king)
                    if not still_check:
                        moves.append(move)
        return moves
    
    def copy(self):
        copy = []

        copy.append(self.white_pieces_on_board.copy())
        copy.append(self.black_pieces_on_board.copy())
        copy.append(self.player_turn)
        copy.append(self.next_player)
        grid_copy = []
        for row in range(self.rows):
            grid_copy.append([])
            for col in range(self.cols):
                grid_copy[row].append(self.grid_2[row][col])
        copy.append(grid_copy)

        return copy

    def revert_from_copy(self, copy):
        
        self.white_pieces_on_board = copy[0]
        self.black_pieces_on_board = copy[1]
        self.player_turn = copy[2]
        self.next_player = copy[3]
        self.grid_2 = copy[4]

    def calculate_legal_moves_2(self, enemy_move):
        self.legal_moves = []
        if self.next_player == WHITE:
            player_pieces = self.white_pieces_on_board
            enemy_pieces = self.black_pieces_on_board
        else:
            player_pieces = self.black_pieces_on_board
            enemy_pieces = self.white_pieces_on_board

        legal_moves_count = 0 # Used to check for stalemate and check
        for i in range(len(player_pieces)-1, -1, -1):
            piece = player_pieces[i]
            if piece.get_pos() == enemy_move:
                player_pieces.pop(i)
                continue

            piece.reset_moves()
            piece.check = False # Reset if piece was previously giving a check

            possible_moves = piece.update_available_moves_2(self.grid_2)
            # Going through each move and checking if it would put the player in check, meaning that it is an illegal move
            for move in possible_moves:
                causes_check = self.hypothetic_move_2(piece, enemy_pieces, move)
                if not causes_check:
                    self.legal_moves.append((piece, move))
                    piece.add_available_move(move)
                    legal_moves_count += 1
            
            if piece.check:
                self.check = True

    def copy(self, with_captured=False):
        copy = [] # index 0 = grid
        grid_copy = []
        for row in range(self.rows):
            grid_copy.append([])
            for col in range(self.cols):
                piece = self.grid[row][col]
                # We will also pass a copy of the state of that piece
                piece_copy = piece.copy_curr_state() if piece != None else None
                grid_copy[row].append((piece, piece_copy))

        copy.append(grid_copy)
        copy.append(self.black_player.score)
        copy.append(self.white_player.score)
        # We copy the pieces on board by getting their positions from grid
        #for piece in self.pieces_on_board
        #copy.append(self.pieces_on_board.copy())
        copy.append(self.player_turn)
        copy.append(self.next_player)
        if with_captured:
            copy.append(self.white_captured.copy())
            copy.append(self.black_captured.copy())

        return copy

    def revert_from_copy(self, copy, with_captured=False):
        grid = copy[0]
        for row in range(self.rows):
            for col in range(self.cols):
                # We check if the piece is at the same position as before, if not we put it there
                curr_piece = self.grid[row][col]
                prev_piece = grid[row][col][0] # Index 0 is the Piece object
                if curr_piece != prev_piece:
                    self.grid[row][col] = prev_piece

                # We also have to move the piece's physical position by using set_pos() which just moves the piece and doesn't calculate other stuff like move_piece()
                # Since the previous piece has moved, that is the one we want to set position of
                if prev_piece != None:
                    # We only want to change the position if there actually was a piece at the square
                    prev_piece.revert_from_copy(grid[row][col][1]) # Index 1 is the copy of the piece state
        #self.grid = copy[0]
        self.black_player.score = copy[1]
        self.white_player.score = copy[2]

        # Set all pieces in pieces_on_board to the pieces from the copy
        white_pieces_on_board_copy = copy[3]
        for i, piece in enumerate(white_pieces_on_board_copy):
            if i < len(self.white_pieces_on_board):
                if self.white_pieces_on_board[i] != piece:
                    self.white_pieces_on_board[i] = piece
            else:
                # Meaning that a piece was delted from the current white_pieces_on_board
                # We have to readd that piece
                self.white_pieces_on_board.append(piece)
        
        black_pieces_on_board_copy = copy[4]
        for i, piece in enumerate(black_pieces_on_board_copy):
            if i < len(self.black_pieces_on_board):
                if self.black_pieces_on_board[i] != piece:
                    self.black_pieces_on_board[i] = piece
            else:
                # Meaning that a piece was delted from the current white_pieces_on_board
                # We have to readd that piece
                self.black_pieces_on_board.append(piece)
        
        pieces_on_board_copy = copy[3]
        self.pieces_on_board.clear()
        for piece in pieces_on_board_copy:
            self.pieces_on_board.append(piece)

        self.player_turn = copy[3]
        self.next_player = copy[4]
        if with_captured:
            self.white_captured = copy[5]
            self.black_captured = copy[6]


    def hypothetic_move_2(self, move_piece, check_pieces, new_square):
        # Check pieces is an array of pieces for which we want to check if they give check after the move is made
        causes_check = False # We set it to false by default
        curr_square = move_piece.get_pos()
        curr_row, curr_col = curr_square

        new_row, new_col = new_square

        prev_piece_at_curr_square = self.grid_2[curr_row][curr_col]
        self.grid_2[curr_row][curr_col] = None 
        piece_at_new_square = self.grid_2[new_row][new_col]

        # COPIES
        original_piece_at_new_square = piece_at_new_square
        original_reference_pawn = None

        # CHECK IF I HAVE DONE THIS PART CORRECTLY MICKI!!!
        if piece_at_new_square and abs(piece_at_new_square) == ENPASSANT and move_piece.type == PAWN:
            if player_turn == WHITE:
                # If it was a white en passant pawn the pawn is above it one row
                piece_at_new_square = self.grid_2[new_row-1][new_col]
                self.grid_2[new_row-1][new_col] = None
            else:
                # If black it is below 1 row
                piece_at_new_square = self.grid_2[new_row+1][new_col]
                self.grid_2[new_row+1][new_col] = None

        # Move piece in grid array to the new position
        self.grid_2[new_row][new_col] = move_piece.type if self.next_player == WHITE else - move_piece.type

        for piece in check_pieces:
            piece.minimax_update_and_add_moves(self.grid_2)

            # Check if the piece is giving check
            if piece.check:
                causes_check = True
                break

        # REVERTING CHANGES
        self.grid_2[curr_row][curr_col] = prev_piece_at_curr_square
        self.grid_2[new_row][new_col] = original_piece_at_new_square

        return causes_check
    
    def handle_game_finished(self):
        if self.result == self.stalemate:
            self.end_box.imgs.append(self.stalemate_text)
            self.end_box.img_positions.append(self.stalemate_text_rect)
        else: # Checkmate
            self.end_box.imgs = [self.checkmate_text]
            self.end_box.img_positions = [self.checkmate_text_rect]
            if self.player_turn == WHITE:
                self.end_box.imgs.append(self.white_won_text)
                self.end_box.img_positions.append(self.white_won_text_rect)
            else:
                self.end_box.imgs.append(self.black_won_text)
                self.end_box.img_positions.append(self.black_won_text_rect)

        self.board_state = self.ended_state

    # Function to get piece from grid from a given position (uses the get_square function)
    def get_piece(self, square):
        row, col = square
        return self.grid[row][col]
    
    # Function to convert a position to the col and row it is in
    def get_square(self, pos):
        gap = self.width // self.rows
        x, y = pos
        y -= self.y
        col = x // gap
        row = y // gap

        return (row, col)
    
    def switch_turn(self):
        self.num_of_moves += 1

        if self.player_turn == WHITE:
            self.player_turn = BLACK
            self.next_player = WHITE
        else:
            self.player_turn = WHITE
            self.next_player = BLACK
            self.curr_move += 1 # Everytime it's white's turn, that means that it's a new move

    def init_pieces(self):
        # BLACK PIECES
        rook = Rook(self.win, BOARD_POSITIONS['a8'], BLACK, self.grid, self.square_size)
        knight = Knight(self.win, BOARD_POSITIONS['b8'], BLACK, self.grid, self.square_size)
        bishop = Bishop(self.win, BOARD_POSITIONS['c8'], BLACK, self.grid, self.square_size)
        queen = Queen(self.win, BOARD_POSITIONS['d8'], BLACK, self.grid, self.square_size)
        self.black_king = King(self.win, BOARD_POSITIONS['e8'], BLACK, self.grid, self.square_size, self.pieces_on_board)
        self.grid[0][0] = rook
        self.grid[0][1] = knight
        self.grid[0][2] = bishop
        self.grid[0][3] = queen
        self.grid[0][4] = self.black_king
        self.grid[0][5] = Bishop(self.win, BOARD_POSITIONS['f8'], BLACK, self.grid, self.square_size)
        self.grid[0][6] = Knight(self.win, BOARD_POSITIONS['g8'], BLACK, self.grid, self.square_size)
        self.grid[0][7] = Rook(self.win, BOARD_POSITIONS['h8'], BLACK, self.grid, self.square_size)
        # BLACK PAWNS
        for i in range(8):
            self.grid[1][i] = Pawn(self.win, (1, i), BLACK, self.grid, self.square_size, self.pieces_on_board, self.en_passant_pieces)
            self.grid_2[1][i] = B_PAWN
        
        # Saving the images for the black pieces so they can be displayed when player needs to choose a piece for pawn promotion
        pawn_img = self.grid[1][0].img
        self.black_piece_imgs = [pawn_img, knight.img, bishop.img, rook.img, queen.img]

        # WHITE PIECES
        rook = Rook(self.win, BOARD_POSITIONS['a1'], WHITE, self.grid, self.square_size)
        knight = Knight(self.win, BOARD_POSITIONS['b1'], WHITE, self.grid, self.square_size)
        bishop = Bishop(self.win, BOARD_POSITIONS['c1'], WHITE, self.grid, self.square_size)
        queen = Queen(self.win, BOARD_POSITIONS['d1'], WHITE, self.grid, self.square_size)
        self.white_king = King(self.win, BOARD_POSITIONS['e1'], WHITE, self.grid, self.square_size, self.pieces_on_board)
        self.grid[7][0] = rook
        self.grid[7][1] = knight
        self.grid[7][2] = bishop
        self.grid[7][3] = queen
        self.grid[7][4] = self.white_king
        self.grid[7][5] = Bishop(self.win, BOARD_POSITIONS['f1'], WHITE, self.grid, self.square_size)
        self.grid[7][6] = Knight(self.win, BOARD_POSITIONS['g1'], WHITE, self.grid, self.square_size)
        self.grid[7][7] = Rook(self.win, BOARD_POSITIONS['h1'], WHITE, self.grid, self.square_size)
        # WHITE PAWNS
        for i in range(8):
            self.grid[6][i] = Pawn(self.win, (6, i), WHITE, self.grid, self.square_size, self.pieces_on_board, self.en_passant_pieces)
            self.grid_2[6][i] = W_PAWN
        
        # Saving the images for the white pieces so they can be displayed when player needs to choose a piece for pawn promotion
        pawn_img = self.grid[6][0].img
        self.white_piece_imgs = [pawn_img, knight.img, bishop.img, rook.img, queen.img]
        
        # Update available moves and threathening variables for every piece on board
        for row in range(self.rows):
            for piece in self.grid[row]:
                if piece != None:
                    piece.reset_moves()
                    piece.update_and_add_available_moves()

                    # Add piece to an array that contains all the pieces, so we can easily loop through them if needed
                    self.pieces_on_board.append(piece)
                    if piece.color == WHITE:
                        self.white_pieces_on_board.append(piece)
                    else:
                        self.black_pieces_on_board.append(piece)
        
        self.grid_2[0][0] = B_ROOK
        self.grid_2[0][1] = B_KNIGHT
        self.grid_2[0][2] = B_BISHOP
        self.grid_2[0][3] = B_QUEEN
        self.grid_2[0][4] = B_KING
        self.grid_2[0][5] = B_BISHOP
        self.grid_2[0][6] = B_KNIGHT
        self.grid_2[0][7] = B_ROOK

        self.grid_2[7][0] = W_ROOK
        self.grid_2[7][1] = W_KNIGHT
        self.grid_2[7][2] = W_BISHOP
        self.grid_2[7][3] = W_QUEEN
        self.grid_2[7][4] = W_KING
        self.grid_2[7][5] = W_BISHOP
        self.grid_2[7][6] = W_KNIGHT
        self.grid_2[7][7] = W_ROOK
        
    def config_game_state(self):
        if self.game_state == NORMAL:
            self.turn_based = True
            self.highlight = True
        elif self.game_state == EXPERIMENTAL:
            self.turn_based = False
            self.highlight = True