import pygame
from constants import *

class Piece():
    def __init__(self, win, pos, color, square_size):
        self.win = win
        self.default_pos = pos
        self.row = pos[0]
        self.col = pos[1]
        self.color = color
        self.img = None
        self.img_center = None
        self.img_size = None
        self.square_size = square_size

        self.available_moves = []
    
    def show(self):
        x = self.col * self.square_size - self.img_center[0] + self.square_size / 2
        #y_margin = (self.square_size - self.img_size[1]) / 2
        y = self.row * self.square_size - self.img_size[1] + self.square_size * 0.98
        self.win.blit(self.img, (x, y))
    
    def move(self):
        pass
    
    def set_img(self, type):
        img_name = 'assets/16x32_pieces/'
        #img_name = 'assets/new_pieces/'
        if self.color == WHITE_PIECE:
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

        # Setting img_center variable
        self.img_center = self.img.get_rect().center
        self.img_size = self.img.get_rect().size