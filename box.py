import pygame

class Box():
    def __init__(self, win, color, pos, width, height, imgs=[], img_positions=[], img_sizes=[]):
        self.win = win
        self.color = color
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.imgs = imgs
        self.img_positions = img_positions
        self.img_sizes = img_sizes
    
    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

        for i, img in enumerate(self.imgs):
            self.win.blit(img, self.img_positions[i])
    
    def clicked_img(self, pos):
        x, y = pos
        
        for i, img_pos in enumerate(self.img_positions):
            img_x, img_y = img_pos
            img_width, img_height = self.img_sizes[i]
            if (x >= img_x and x <= img_x + img_width) and (y >= img_y and y <= img_y + img_height):
                return i
        
        # We return -1 to indicate that no img was clicked
        return -1

# REFERENCE FOR PREVIOUS WAY OF DRAWING BOX
'''
margin_between_pieces = self.piece_img_size[0]
self.box_height = self.square_size * 2
self.box_width = self.piece_img_size[0] * 5 + margin_between_pieces * 6
self.box_x = self.pos[0] + (self.width / 2) - (self.box_width / 2)
self.box_y = self.pos[1] + (self.height / 2) - (self.box_height / 2)
self.promotion_img_positions = [] # Index 0 = pawn, 1 = knight, 2 = bishop, 3 = rook, 4 = queen

self.win.blit(self.grey_overlay, self.pos)
pygame.draw.rect(self.win, (200, 200, 200), (self.box_x, self.box_y, self.box_width, self.box_height))

if self.promotion_color == WHITE:
    imgs = self.white_piece_imgs
else:
    imgs = self.black_piece_imgs

for i, img in enumerate(imgs):
    img_x, img_y = self.promotion_img_positions[i]
    self.win.blit(img, (img_x, img_y))
'''