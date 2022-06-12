import pygame
from piece import Piece

class Knight(Piece):
    def __init__(self, win, pos, color, square_size):
        super().__init__(win, pos, color, square_size)
        self.set_img('Knight')

