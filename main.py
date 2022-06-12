import pygame
from board import Board

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Game():
    def __init__(self, win, width, height):
        pygame.init()
        self.win = win
        self.width = width
        self.height = height
        self.bg = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running, self.pause, self.exit, self.menu = 1, 2, 3, 4
        self.state = self.running

        self.board_width, self.board_height = self.width, self.height
        self.board_x, self.board_y = 0, 0
        self.board = Board(self.win, (self.board_x, self.board_y), (self.board_width, self.board_height))

        self.dots = []
    
    def run(self):
        while True:
            # Game running state
            if self.state == self.running:
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
                self.dots.append(pos)

                if (pos[0] >= self.board_x and pos[0] <= self.board_x + self.board_width) and (pos[1] >= self.board_y and pos[1] <= self.board_y + self.board_height):
                    self.board.mouse_clicked(pos)
    
    def update(self):
        pass

    def clear_screen(self):
        self.win.fill(self.bg)
    
    def draw(self):
        self.board.show()
        self.draw_dots()
    
    def draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(self.win, (255, 0, 0), dot, 2)

if __name__ == "__main__":
    game = Game(WIN, WIDTH, HEIGHT)
    game.run()


