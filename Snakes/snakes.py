import pygame
import sys
import time
import random


class Snake:

    def __init__(self):
        self.snake_color = 0, 255, 0
        self.direction = 'right'
        self.size = 10
        self.snake_pos = [200,200]
        self.snake_body= [[200, 200], [200-10, 200], [200-(10*2), 200], [200-(10*3), 200]]

    #def get_snake_body(self):
        #snake_body_pos = [[200, 200], [200-10, 200], [200-(10*2), 200]

    def clear_screen(self, screen):
        screen.fill((0,0,0))

    def draw(self,screen):
        for square in self.snake_body:
            pygame.draw.rect(screen, self.snake_color, pygame.Rect(square[0], square[1], self.size, self.size))
        self.turn()
        self.snake_body.append(list(self.snake_pos))
        self.snake_body.pop(0)
        pygame.display.flip()
        self.clear_screen(screen)

    def turn(self):
        if self.direction == 'left':
            self.snake_pos[0] -= 10
        elif self.direction == 'right':
            self.snake_pos[0] += 10
        elif self.direction == 'up':
            self.snake_pos[1] -= 10
        elif self.direction == 'down':
            self.snake_pos[1] += 10

    def game_over(self):
        if self.snake_pos[0] >= self.height or self.snake_pos[1] <= -5:
            sys.exit()
        elif self.snake_pos[0] >= self.width or self.snake_pos[1] <= -5:
            sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.unicode == 'w' and self.direction != 'down':
                    self.direction = 'up'
                if event.unicode == 's' and self.direction != 'up':
                    self.direction = 'down'
                if event.unicode == 'a' and self.direction != 'right' :
                    self.direction = 'left'
                if event.unicode == 'd' and self.direction != 'left':
                    self.direction = 'right'
                if event.unicode == 'p':
                    if pause == False:
                        pause = True
                    else:
                        pause = False                

class Fruit:
    def __init__(self):
        pass

BOARD_SIZE = WIDTH, HEIGHT = 800, 600
BG_COLOR = 0, 0, 0
FRUIT_COLOR = 255, 255, 255
COLOR = 255, 0, 0     

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(BOARD_SIZE)
    font_style = pygame.font.SysFont(None, 50)
    pause = False

    snake = Snake()
    fruit = Fruit()

    while True:
        snake.draw(screen)
        snake.handle_events()
        clock.tick(20)

main()