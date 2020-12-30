import pygame
import sys
import time

BOARD_SIZE = WIDTH, HEIGHT = 800, 600
BG_COLOR = 0, 0, 0
SNAKE_COLOR = 0, 255, 0
SIZE = 10

class Snake_Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(BG_COLOR)

    def render(self):
        self.clear_screen()
        pygame.draw.rect(self.screen, SNAKE_COLOR, pygame.Rect(self.j, self.i, SIZE, SIZE))  
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'w':
                    self.i -= 10
                if event.unicode == 's':
                    self.i += 10
                if event.unicode == 'a':
                    self.j -= 10
                if event.unicode == 'd':
                    self.j += 10

    def run(self):
        self.j = 400
        self.i = 300
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(20)
            

game = Snake_Game()
game.run()