import pygame
from constants import *

class Piece():
    def __init__(self, win, pos, color, board, square_size):
        self.win = win
        self.default_pos = pos
        self.row = pos[0]
        self.col = pos[1]
        self.color = color
        self.board = board
        self.img = None
        self.img_center = None
        self.img_default_size = None
        self.img_minimized_size = None
        self.img_size = None
        self.square_size = square_size
        self.type = None
        self.en_passant_piece = False
        self.check = False

        self.first_move = True
        self.possible_moves = [] # This is the moves before they have been checked if they cause check
        self.available_moves = [] # This is all the legal moves the piece can make
        self.threathening = []

        # Values of each piece
        self.value = 1
    
    def show(self, y_margin):
        x = self.col * self.square_size - self.img_center[0] + self.square_size / 2
        #y_margin = (self.square_size - self.img_size[1]) / 2
        y = self.row * self.square_size - self.img_size[1] + self.square_size * 0.98
        # Set y position relative to board position
        y += y_margin
        self.win.blit(self.img, (x, y))
    
    def move(self, new_square):
        row, col = new_square
        self.row = row
        self.col = col

        # Not first move anymore
        self.first_move = False

    def valid_move(self, row, col):
        return (row >= 0 and row < 8) and (col >= 0 and col < 8)
    
    def set_img(self, type):
        img_name = 'assets/16x32_pieces/'
        #img_name = 'assets/new_pieces/'
        if self.color == WHITE:
            img_name += 'W_'
        else:
            img_name += 'B_'
        
        img_name += type + '.png'
        
        # Setting the image to the correct color and piece
        self.img = pygame.image.load(img_name)
        img_rect = self.img.get_rect()

        # Scaling image by finding the number that will make height of piece the same as square_size
        img_width = img_rect.size[0]
        img_height = img_rect.size[1]
        #img_scl = self.square_size / 29
        img_scl = self.square_size / (PIECE_IMG_SIZE[1]-3)
        self.img = pygame.transform.scale(self.img, (img_width * img_scl, img_height * img_scl))

        # Setting img_center variable and size variables
        self.img_center = self.img.get_rect().center
        self.img_size = self.img.get_rect().size

        self.img_default_size = self.img
        mini_size = (self.img_size[0] * 0.55, self.img_size[1] * 0.55)
        self.img_minimized_size = pygame.transform.scale(self.img, mini_size)
    
    def set_default_size(self):
        #self.img_size = self.img_default_size
        #self.img = pygame.transform.scale(self.img, self.img_size)
        self.img = self.img_default_size
    
    def set_minimized_size(self):
        #self.img_size = self.img_minimized_size
        #self.img = pygame.transform.scale(self.img, self.img_size)

        self.img = self.img_minimized_size
    
    def get_pos(self):
        return (self.row, self.col)
    
    def set_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]
    
    def copy_curr_state(self):
        copy = [] # Index 0 = img size, 1 = available_moves, 2 = position, 3 = promoted or en passant move state, 4 = pawn first move
        copy.append(self.available_moves.copy())
        copy.append(self.get_pos())
        copy.append(self.first_move)
        if self.type == PAWN:
            copy.append(self.promote) # Wether or not the pawn was promoted
        elif self.type == ENPASSANT:
            copy.append(self.move) # The current state of an en passant pawn
            copy.append(self.killed)
        
        return copy
    
    def revert_from_copy(self, copy):
        if self.img:
            self.set_default_size()

        self.available_moves = copy[0]
        self.set_pos(copy[1])
        self.first_move = copy[2]

        if self.type == PAWN:
            self.promote = copy[3]
        elif self.type == ENPASSANT:
            self.move = copy[3]
            self.killed = copy[4]
    
     # Finds the start and end squares that make up the diagonals the bishop moves on
    def calculate_diag_edges(self):
         # Start by finding start square for right diag and end square for left diag
        # These are the two squares closest to bottom of board
        start_row_right = 7
        end_row_left = 7
        # This col is found by seeing how far the piece is from the first row. Then moving that amount to the left (subtracting from current col)
        start_col_right = self.col - (7 - self.row)
        end_col_left = self.col + (7 - self.row) # For the left diag we just move to the right (this will be the col for the end square)
        if start_col_right < 0:
            # The amount that goes below zero is row value taken from bottom
            row_from_bottom = start_col_right * -1
            start_row_right = 7 - row_from_bottom # We subtract it with 7 because it's the row value from bottom, and we multiply by -1 just to make the number positive
            start_col_right = 0
        
        start_square_right_diag = (start_row_right, start_col_right)

        if end_col_left > 7:
            row_from_bottom = end_col_left - 7 # This is a positive number, so we dont need to multiply by 1
            end_row_left = 7 - row_from_bottom # Same as above
            end_col_left = 7 # Set end column to the max
        
        end_square_left_diag = (end_row_left, end_col_left)
        # Now that we have found the start square for the right diag aswell as the end square for the left diag, we need to find the other two
        # These are the two squares closest to the top of the board
        # Same logic can be used to find these two

        end_row_right = 0 # First we set a default value for the row which is 0 in most cases
        start_row_left = 0 # Again we just presume without knowing anything that the row is the top row

        end_col_right = self.col + self.row
        start_col_left = self.col - self.row
        if end_col_right > 7:
            # The amount that goes above 7 is the value of the row (MATH)
            end_row_right = end_col_right - 7
            end_col_right = 7
        
        end_square_right_diag = (end_row_right, end_col_right)

        if start_col_left < 0:
            start_row_left = start_col_left * -1
            start_col_left = 0
        
        start_square_left_diag = (start_row_left, start_col_left)

        return start_square_right_diag, end_square_right_diag, start_square_left_diag, end_square_left_diag

    # ALSO UPDATES THREATHENING VARIABLE
    def check_moves_diag(self, start_square, end_square, left_diag=False):
        # By default this function will check squares on the right_diag
        row_inc = -1
        col_inc = 1
        if left_diag:
            # We are checking the diag from top left --> bottom right
            # Therefore we will increment curr_row by 1 and also increment curr_col by 1 in the for loop
            row_inc = 1
            col_inc = 1


        # Now we will loop through all the right diag squares
        available_diag = []
        min_diag = 0
        max_diag = 7

        threathening_left = None # Temporary variable that is used in order to find the closest piece to the left of the bishop that it's threathening

        curr_row, curr_col = start_square
        for col in range(start_square[1], end_square[1]+1):
            piece = self.board[curr_row][curr_col]

            if curr_col != self.col:
                # Only add the square if it is not the current position of the bishop
                available_diag.append((curr_row, curr_col))
            if piece != None and piece.type != ENPASSANT:
                # If there is a piece at this square
                if curr_col < self.col:
                    # If the piece is to the left of this bishop we will set the right_diag_min to this square, as it's temporarily the best guess
                    min_diag = (curr_row, curr_col)

                    # This is also the piece that the bishop or queen is threathening
                    threathening_left = piece

                    # If we encounter a piece closer to the rook, we will also reset the available moves up until now
                    # Because we are in this if statement, it means that we have encountered a piece to the left of the bishop on this diag that is closer than the other one
                    # Therefore we want to reset the available moves added up until now
                    available_diag = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece.color != self.color:
                        available_diag.append((curr_row, curr_col))
                elif curr_col > self.col:
                    # This if statement is executed if the piece is to the right of the bishop
                    # If a piece is encountered here, we want to set that square as the limit, since it's the first piece to the right of the bishop
                    max_diag = (curr_row, curr_col)

                    # Check to see if this piece is the opponents piece
                    if piece.color != self.color:
                        self.add_threathening(piece) # BISHOP THREATHENS TO CAPTURE THIS PIECE
                    else:
                        # If it is a piece from the same side then we will remove the last position added to available_right_diag, as we can't capture our own pieces
                        available_diag.pop()
                    break # It's important that we break since the first piece encountered to the right, will be the limit as to where the bishop can move

            # At the end of the for loop we will go to the next square on diag
            curr_row += row_inc
            curr_col += col_inc

        # If the closest piece to the left of the bishop is an opponent piece, it will be stored in threathening_left
        if threathening_left != None:
            # Only append if it is an oponent piece
            if threathening_left.color != self.color:
                self.add_threathening(threathening_left)
        
        return available_diag
    
    # ALSO UPDATES THREATHENING VARIABLE
    def check_moves_straight(self):
        min_horizontal = 0
        max_horizontal = 7
        available_horizontal = []
        min_vertical = 0
        max_vertical = 7
        available_vertical = []

        threathening_curr = None # Temporary variable that is used in order to find the closest piece to the rook that it's threathening

        # Check horizontal direction
        for col, piece in enumerate(self.board[self.row]):
            if col != self.col:
                # Only add position if it is not the current position of the rook
                available_horizontal.append((self.row, col))
            
            if piece != None and piece.type != ENPASSANT:
                if col < self.col:
                    # If there is a piece we will set that as the new min_horizontal, as we can't go past that piece
                    min_horizontal = col
                    threathening_curr = piece

                    # If we encounter a piece closer to the rook, we will also reset the available moves up until now
                    available_horizontal = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece.color != self.color:
                        available_horizontal.append((self.row, col))
                elif col > self.col:
                    # If col is greater than the column where this rook is, then it's the new max_horizontal
                    max_horizontal = col

                    # Check to see if this piece is the opponents piece
                    if piece.color != self.color:
                        self.add_threathening(piece) # ROOK THREATHENS TO CAPTURE THIS PIECE
                    else:
                        # If it is a piece from the same side then we will remove the last position added to available_horizontal, as we can't capture our own pieces
                        available_horizontal.pop()
                    break # It's important that we break since the first piece encountered to the right, will be the limit as to where the rook can move
        
        # If rook was threathening a piece to the left, the threathening_curr variable will not be None
        if threathening_curr != None:
            # Only append if it is an oponent piece
            if threathening_curr.color != self.color:
                self.add_threathening(threathening_curr)
            threathening_curr = None # Reset it so it can be used when analyzing the vertical axis

        # Check vertical direction
        for row in range(8):
            piece = self.board[row][self.col] # This will check all the pieces on the vertical line of the rook
            
            if row != self.row:
                # Only add position if it is not the current position of the rook
                available_vertical.append((row, self.col))
            if piece != None:
                if row < self.row:
                    min_vertical = row # This will update the vertical move for the rook until it encounters the closest piece to the rook
                    threathening_curr = piece

                    available_vertical = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece.color != self.color:
                        available_vertical.append((row, self.col))
                elif row > self.row:
                    max_vertical = row

                    if piece.color != self.color:
                        self.add_threathening(piece) # ROOK THREATHENS TO CAPTURE THIS PIECE
                    else:
                        # If it is a piece from the same side then we will remove the last position added to available_vertical, as we can't capture our own pieces
                        available_vertical.pop()
                    break # Again we have to break, as we only want the closest piece to the rook
        
        if threathening_curr != None:
             # Only append if it is an oponent piece
            if threathening_curr.color != self.color:
                self.add_threathening(threathening_curr)
        
        return available_horizontal + available_vertical
    
    def is_threathening(self, square):
        for move in self.available_moves:
            if move == square:
                return True
        return False

    def add_threathening(self, piece):
        self.threathening.append(piece)
        if piece.type == KING:
            self.check = True
    
    def add_available_move(self, move):
        self.available_moves.append(move)
        if self.board[move[0]][move[1]] != None and self.board[move[0]][move[1]].type == KING:
            self.check = True
    
    def update_available_moves(self):
        # Gets overritten by every inherited class
        pass
    
    def update_and_add_available_moves(self):
        self.update_available_moves() # Sets all possible moves variable
        for move in self.possible_moves:
            self.add_available_move(move)
    
    def minimax_update_and_add_moves(self, board):
        self.available_moves = self.update_available_moves_2(board)

    
    def reset_moves(self):
        self.possible_moves = []
        self.available_moves = []
        self.threathening = []
        self.check = False
    
    def check_moves_diag_2(self, start_square, end_square, board=None, left_diag=False):
        # By default this function will check squares on the right_diag
        row_inc = -1
        col_inc = 1
        if left_diag:
            # We are checking the diag from top left --> bottom right
            # Therefore we will increment curr_row by 1 and also increment curr_col by 1 in the for loop
            row_inc = 1
            col_inc = 1


        # Now we will loop through all the right diag squares
        available_diag = []
        min_diag = 0
        max_diag = 7

        curr_row, curr_col = start_square
        for col in range(start_square[1], end_square[1]+1):
            piece = board[curr_row][curr_col]

            if curr_col != self.col:
                # Only add the square if it is not the current position of the bishop
                available_diag.append((curr_row, curr_col))
            if piece != None and abs(piece) != ENPASSANT:
                piece_color = WHITE if piece > 0 else BLACK
                # If there is a piece at this square
                if curr_col < self.col:
                    # If the piece is to the left of this bishop we will set the right_diag_min to this square, as it's temporarily the best guess
                    min_diag = (curr_row, curr_col)

                    # If we encounter a piece closer to the rook, we will also reset the available moves up until now
                    # Because we are in this if statement, it means that we have encountered a piece to the left of the bishop on this diag that is closer than the other one
                    # Therefore we want to reset the available moves added up until now
                    available_diag = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece_color != self.color:
                        if abs(piece) == KING:
                            self.check = True
                        available_diag.append((curr_row, curr_col))
                elif curr_col > self.col:
                    # This if statement is executed if the piece is to the right of the bishop
                    # If a piece is encountered here, we want to set that square as the limit, since it's the first piece to the right of the bishop
                    max_diag = (curr_row, curr_col)

                    # Check to see if this piece is the opponents piece
                    if piece_color == self.color:
                        available_diag.pop()
                    elif abs(piece) == KING:
                        self.check = True
                    break # It's important that we break since the first piece encountered to the right, will be the limit as to where the bishop can move

            # At the end of the for loop we will go to the next square on diag
            curr_row += row_inc
            curr_col += col_inc
        
        return available_diag

    def check_moves_straight_2(self, board=None):
        min_horizontal = 0
        max_horizontal = 7
        available_horizontal = []
        min_vertical = 0
        max_vertical = 7
        available_vertical = []

        # Check horizontal direction
        for col, piece in enumerate(board[self.row]):
            if col != self.col:
                # Only add position if it is not the current position of the rook
                available_horizontal.append((self.row, col))
            
            if piece != None:
                piece_type = abs(piece)
                if piece_type == ENPASSANT:
                    continue
                piece_color = WHITE if piece > 0 else BLACK
                if col < self.col:
                    # If there is a piece we will set that as the new min_horizontal, as we can't go past that piece
                    min_horizontal = col

                    # If we encounter a piece closer to the rook, we will also reset the available moves up until now
                    available_horizontal = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece_color != self.color:
                        if abs(piece) == KING:
                            self.check = True
                        available_horizontal.append((self.row, col))
                elif col > self.col:
                    # If col is greater than the column where this rook is, then it's the new max_horizontal
                    max_horizontal = col

                    # Check to see if this piece is the opponents piece
                    if piece_color == self.color:
                        available_horizontal.pop()
                    elif abs(piece) == KING:
                        self.check = True
                    break # It's important that we break since the first piece encountered to the right, will be the limit as to where the rook can move
        
        # Check vertical direction
        for row in range(8):
            piece = board[row][self.col] # This will check all the pieces on the vertical line of the rook
           
            
            if row != self.row:
                # Only add position if it is not the current position of the rook
                available_vertical.append((row, self.col))
            if piece != None:
                piece_color = WHITE if piece > 0 else BLACK
                if row < self.row:
                    min_vertical = row # This will update the vertical move for the rook until it encounters the closest piece to the rook

                    available_vertical = []
                    # However we will add this current position to available moves if it's one of opponents pieces, as it will be a capturing move
                    if piece_color != self.color:
                        if abs(piece) == KING:
                            self.check = True
                        available_vertical.append((row, self.col))
                elif row > self.row:
                    max_vertical = row

                    if piece_color == self.color:
                        available_vertical.pop()
                    elif abs(piece) == KING:
                        self.check = True
                    break
        
        return available_horizontal + available_vertical
        