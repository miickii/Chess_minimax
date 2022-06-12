from piece import Piece
import pygame
from king import King
from rook import Rook
from knight import Knight
from queen import Queen
from pawn import Pawn
from bishop import Bishop
from constants import *

class Board():
    def __init__(self, win, pos, board_size):
        self.win = win
        self.pos = pos
        self.width = board_size[0]
        self.height = board_size[1]
        self.rows, self.cols = 8, 8
        self.grid = []
        # Filling board with None
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(None)

        self.square_size = self.width / 8
        self.highlighted_squares = []
        self.squares = [] # 2d array of surfaces for each square on board
        for i in range(self.rows):
            self.squares.append([])
            for j in range(self.cols):
                square = pygame.Surface((self.square_size, self.square_size))
                square.set_alpha(150)
                square.fill((255, 0, 0))
                self.squares[i].append(square)

        self.img = pygame.image.load('assets/extras/board3_2.png')
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        self.selected_piece = None
        self.move_state = False

        self.init_pieces()

    
    def run(self):
        pass

    
    def show(self):
        self.win.blit(self.img, self.pos)

        for row in range(self.rows):
            for piece in self.grid[row]:
                if piece: # Square in grid is not None, but a Piece object
                    piece.show()
        
        for arr in self.highlighted_squares:
            square = arr[0]
            pos = arr[1]
            # The pos is in the form of column and row, so it has to be scaled by the square_size
            x = pos[1] * self.square_size # The column position
            y = pos[0] * self.square_size # The row position
            self.win.blit(square, (x, y))
    
    def mouse_clicked(self, pos):
        # First check if a piece has already been selected and a move is about to take place
        if self.move_state:
            clicked_square = self.get_square(pos)
            # Check if the clicked_square is any of the squares in highlighted_squares
            for square in self.highlighted_squares:
                square_pos = square[1]
                if square_pos == clicked_square:
                    # Meaning that the move is among one of the available moves
                    # If that's the case we want to move the piece
                    self.move_piece()
            
            if self.move_state:
                # If the player doesn't click a valid square for the piece it means that they either deselected the piece or chose another piece.
                # In that case, the move_state will still be true as the move_piece() function hasn't been called
                # move_state should be False and we want to check if the player clicked another piece instead
                self.move_state = False
                self.update_selected_piece(pos)
        else: # If not the case, we want to check if the player has selected a piece
            self.update_selected_piece(pos)

    # Function to check if the player has clicked a piece on the board. If so, we want to highlight available moves
    def update_selected_piece(self, pos):
        self.selected_piece = self.get_piece(pos)
        if self.selected_piece != None:
            # Highligt available moves
            self.highlighted_squares = [] # Resetting current highlighted squares
            self.highlight_squares(self.selected_piece.available_moves)
            print(self.highlighted_squares)
            self.move_state = True
        else:
            # Stop rendering any highlighted squares
            self.highlighted_squares = []
            self.move_state = False
    
    def move_piece(self):
        # CODE FOR MOVING THE PIECE
        curr_square = (self.selected_piece.row, self.selected_piece.col)
        new_square = self.selected_piece.move() # Moves the piece and get's the new col and row of its position

        # Move piece in grid variable
        self.grid[curr_square[0]][curr_square[1]] = None
        self.grid[new_square[0]][new_square[1]] = self.selected_piece

        # If the player moves, we are no longer in the move_state, the highlighted squares should not render, and we have to update the available moves for the moved piece.
        self.selected_piece.update_available_moves()
        self.highlighted_squares = []
        self.move_state = False
        self.selected_piece = None # This is redundant but a good idea

    def highlight_squares(self, positions):
        for pos in positions:
            square = self.squares[pos[0]][pos[1]] # Retrieve the square corresponding to the position
            self.highlighted_squares.append([square, pos]) # Adding that square to the current highlighted squares, so it will be rendered to the window. We also add the position for when it get's blittet to the screen

    # Function to get piece from grid from a given position (uses the get_square function)
    def get_piece(self, pos):
        row, col = self.get_square(pos)
        return self.grid[row][col]
    
    # Function to convert a position to the col and row it is in
    def get_square(self, pos):
        gap = self.width // self.rows
        x, y = pos
        col = x // gap
        row = y // gap

        return (row, col)

    def init_pieces(self):
        # BLACK PIECES
        self.grid[0][0] = Rook(self.win, BOARD_POSITIONS['a8'], BLACK_PIECE, self.square_size)
        self.grid[0][1] = Knight(self.win, BOARD_POSITIONS['b8'], BLACK_PIECE, self.square_size)
        self.grid[0][2] = Bishop(self.win, BOARD_POSITIONS['c8'], BLACK_PIECE, self.square_size)
        self.grid[0][3] = Queen(self.win, BOARD_POSITIONS['d8'], BLACK_PIECE, self.square_size)
        self.grid[0][4] = King(self.win, BOARD_POSITIONS['e8'], BLACK_PIECE, self.square_size)
        self.grid[0][5] = Bishop(self.win, BOARD_POSITIONS['f8'], BLACK_PIECE, self.square_size)
        self.grid[0][6] = Knight(self.win, BOARD_POSITIONS['g8'], BLACK_PIECE, self.square_size)
        self.grid[0][7] = Rook(self.win, BOARD_POSITIONS['h8'], BLACK_PIECE, self.square_size)
        # BLACK PAWNS
        for i in range(8):
            self.grid[1][i] = Pawn(self.win, (1, i), BLACK_PIECE, self.square_size)

        # WHITE PIECES
        self.grid[7][0] = Rook(self.win, BOARD_POSITIONS['a1'], WHITE_PIECE, self.square_size)
        self.grid[7][1] = Knight(self.win, BOARD_POSITIONS['b1'], WHITE_PIECE, self.square_size)
        self.grid[7][2] = Bishop(self.win, BOARD_POSITIONS['c1'], WHITE_PIECE, self.square_size)
        self.grid[7][3] = Queen(self.win, BOARD_POSITIONS['d1'], WHITE_PIECE, self.square_size)
        self.grid[7][4] = King(self.win, BOARD_POSITIONS['e1'], WHITE_PIECE, self.square_size)
        self.grid[7][5] = Bishop(self.win, BOARD_POSITIONS['f1'], WHITE_PIECE, self.square_size)
        self.grid[7][6] = Knight(self.win, BOARD_POSITIONS['g1'], WHITE_PIECE, self.square_size)
        self.grid[7][7] = Rook(self.win, BOARD_POSITIONS['h1'], WHITE_PIECE, self.square_size)
        # WHITE PAWNS
        for i in range(8):
            self.grid[6][i] = Pawn(self.win, (6, i), WHITE_PIECE, self.square_size)