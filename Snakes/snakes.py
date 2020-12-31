import pygame
import sys
import time
import random

class Snake:

    def __init__(self):
        self.height = HEIGHT
        self.width = WIDTH
        self.snake_grow = False
        self.snake_color = 0, 255, 0
        self.font_style = pygame.font.SysFont(None, 50)
        self.direction = 'left'
        self.size = 10
        self.snake_pos = [200,200]
        self.snake_body= [[200, 200], [200-10, 200], [200-(10*2), 200]]

    def clear_screen(self, screen):
        screen.fill((0,0,0))

    def display_message(self, msg, screen):
        mesg = self.font_style.render(msg, True, (255,0,0))
        screen.blit(mesg, [WIDTH//2, HEIGHT//2])
        pygame.display.flip()

    def draw(self, screen, snake_grow):
        for square in self.snake_body:
            pygame.draw.rect(screen, self.snake_color, pygame.Rect(square[0], square[1], self.size, self.size))

        self.game_over(screen)
        self.turn()
        self.snake_body.append(list(self.snake_pos))

        if snake_grow == False:
            self.snake_body.pop(0)

        for square in self.snake_body[1:(len(self.snake_body)-1)]:
            if pygame.Rect(square[0],square[1],10,10).colliderect(pygame.Rect(self.snake_pos[0], self.snake_pos[1],10,10)):
                msg = 'GAME OVER'
                self.display_message(msg, screen)
                time.sleep(2)
                sys.exit()

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

    def game_over(self, screen):
        if self.snake_pos[1] >= self.height + 10 or self.snake_pos[1] <= -10:
            msg = 'GAME OVER'
            self.display_message(msg, screen)
            time.sleep(2)
            sys.exit()
        elif self.snake_pos[0] >= self.width + 10 or self.snake_pos[0] <= -10:
            msg = 'GAME OVER'
            self.display_message(msg, screen)
            time.sleep(2)
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
        self.fruit_pos = [100,100]
        self.fruit_color = 255, 255, 255
        self.size = 10

    def spawn_fruit(self):
        self.fruit_pos = [random.randint(0, WIDTH-10), random.randint(0, HEIGHT-10)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.fruit_color, pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], self.size, self.size))

BOARD_SIZE = WIDTH, HEIGHT = 800, 600 

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(BOARD_SIZE)
    
    pause = False
    snake_grow = False

    snake = Snake()
    fruit = Fruit()

    while True:
        snake.draw(screen, snake_grow) 
        snake_grow = False      
        snake_x, snake_y = snake.snake_pos[0], snake.snake_pos[1]
        fruit_x, fruit_y = fruit.fruit_pos[0], fruit.fruit_pos[1]

        if pygame.Rect(snake_x, snake_y,10,10).colliderect(pygame.Rect(fruit_x, fruit_y,10,10)):
            fruit.spawn_fruit()
            snake_grow = True

        fruit.draw(screen)
        snake.handle_events()
        clock.tick(20)

main()