import pygame
import sys
import re # Regex
from board import Board
from player import Player
from constants import *

WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess minimax algorithm')

class Game():
    def __init__(self, win, width, height, args):
        pygame.init()
        self.args = args
        self.win = win
        self.width = width
        self.height = height
        self.bg = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running, self.running_debug, self.pause, self.exit, self.menu = 1, 2, 3, 4, 5
        if len(self.args) > 1:
            self.state = self.running_debug
        else:
            self.state = self.running

        self.auto_game = False
        game = ENPASSANT_CHECKMATE
        self.game_moves = self.convert_game_to_moves(game)
        #print(self.game_moves)

        self.board_width, self.board_height = 600, 600
        self.board_x, self.board_y = 0, (self.height - self.board_height) / 2
        self.board = Board(self.win, (self.board_x, self.board_y), (self.board_width, self.board_height), NORMAL)

        self.player_white = Player(WHITE, self.board, ai=False, ai_level=3, depth=1)
        self.player_black = Player(BLACK, self.board, ai=True, ai_level=3, depth=3)
        self.board.white_player = self.player_white
        self.board.black_player = self.player_black

        self.mouse_clicked = False
        self.mouse_pos = None
        self.dots = []

        self.game_start_sound = pygame.mixer.Sound("assets/sound/game_start.wav")
        pygame.mixer.Sound.play(self.game_start_sound)
        pygame.mixer.music.stop()
    
    def run(self):
        while True:
            # Game running state
            if self.state == self.running_debug:
                self.handle_events()
                self.update()
                self.clear_screen()
                self.draw()
                pygame.display.update()
            elif self.state == self.running:
                self.handle_events()
                self.update()
                self.clear_screen()
                self.draw()
                pygame.display.update()
            # Exiting state
            elif self.state == self.exit:
                break
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = self.exit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.mouse_pos = pos
                #self.dots.append(pos)

                if (pos[0] >= self.board_x and pos[0] <= self.board_x + self.board_width) and (pos[1] >= self.board_y and pos[1] <= self.board_y + self.board_height):
                    self.mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.board.pop()
    
    def update(self):
        curr_player = self.board.player_turn

        if self.board.board_state != self.board.ended_state:
            move_count = self.board.curr_move - 1
            move = ""
            if self.auto_game:
                if curr_player == WHITE:
                    move = self.game_moves[move_count][0]
                elif curr_player == BLACK:
                    move = self.game_moves[move_count][1]
                '''elif (self.player_black.ai == True and curr_player == BLACK) or (self.player_white.ai == True and curr_player == WHITE):
                    self.board.random_move()'''
            elif (self.player_black.ai == True and curr_player == BLACK):
                self.player_black.make_move()
            elif (self.player_white.ai == True and curr_player == WHITE):
                self.player_white.make_move()
                pygame.time.delay(50)
            elif self.mouse_clicked:
                self.board.mouse_clicked(self.mouse_pos)
                self.mouse_clicked = False

            
            if move != "":
                pygame.time.delay(200)
                self.board.make_move(move)


    def clear_screen(self):
        self.win.fill(self.bg)
    
    def draw(self):
        self.board.show()
        self.draw_dots()
    
    def draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(self.win, C_BLUE, dot, 2)
    
    def convert_game_to_moves(self, game):
        separated = game.split(".")
        moves = []
        for move in separated:
            m = re.split("(?<!\S)\d+(?!\S)", move)[0] # Regex looking for a single digit standing alone. Selecting the first element, which is the move
            if m != "": # The first move will be empty using this combination of regex functions
                m = m.split(" ") # Separates the white move and the black move
                # With this regex m will have an empty value at index 2 if it isn't the last move. We have to remove that
                if m[-1] == '':
                    m.pop(-1)
                if m[0] == '':
                    m.pop(0)
                moves.append(m)
        
        return moves

if __name__ == "__main__":
    args = sys.argv
    game = Game(WIN, WIDTH, HEIGHT, args)
    game.run()


