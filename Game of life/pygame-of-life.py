#! python3

import pygame
import os
import sys,time
import random


BOARD_SIZE = WIDTH,HEIGHT = 650, 650
DEAD = 0, 0, 0
ALIVE = 0, 255, 150
CELL_SIDE = 5
BG = 0, 0, 0


class LifeGame:
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pygame.display.flip()

        self.clock = pygame.time.Clock()
        
        self.num_cols = int(WIDTH / 10)
        self.num_rows = int(HEIGHT / 10)
        self.grids = []
        self.active_grid = 0
        self.init_grids()

    def init_grids(self):

        def create_grids():
            rows = []
            for r in range(self.num_rows):
                coloums = [0] * self.num_cols
                rows.append(coloums)
            return rows
        
        self.grids.append(create_grids())
        self.grids.append(create_grids())
        #self.set_grid()


    def set_grid(self, value = None, grid = 0):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value
        self.grids[grid][0][0] = 1

    def get_cell(self,r,c):
        try:
            cell_value = self.grids[self.active_grid][r][c]
        except:
            cell_value = 0
        return cell_value

    def check_neighbours(self,r,c):
        num_alive_neighbours = 0
        # Getting alive neighbours
        num_alive_neighbours += self.get_cell(r - 1, c - 1)
        num_alive_neighbours += self.get_cell(r - 1, c)
        num_alive_neighbours += self.get_cell(r - 1, c + 1)
        num_alive_neighbours += self.get_cell(r, c - 1)
        num_alive_neighbours += self.get_cell(r, c + 1)
        num_alive_neighbours += self.get_cell(r + 1, c - 1)
        num_alive_neighbours += self.get_cell(r + 1, c)
        num_alive_neighbours += self.get_cell(r + 1, c + 1)

        # Rules of life and death
        if self.grids[self.active_grid][r][c] == 1: # Alive
            if num_alive_neighbours >= 4: # Overpopulation
                return 0

            elif num_alive_neighbours <=1: # Underpopulation
                return 0

            elif num_alive_neighbours == 3 or 2: #survive
                return 1

        elif self.grids[self.active_grid][r][c] == 0: # Dead
            if num_alive_neighbours == 3:
                return 1 # Come alive

        return self.grids[self.active_grid][r][c]

    def inactive_grid(self):
        return (self.active_grid + 1) % 2


    def update_gen(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_gen_state = self.check_neighbours(r,c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()


    def clear_screen(self):
        self.screen.fill(BG)

    def draw_grid(self):
        self.clear_screen()
        for c in range(self.num_rows):
            for r in range(self.num_cols):
                if self.grids[self.active_grid][r][c] == 1:
                    color = ALIVE
                else:
                    color = DEAD
                pygame.draw.rect(self.screen,
                                 color,
                                 ((c * 10 + 5),
                                  (r * 10 + 5),
                                   CELL_SIDE, CELL_SIDE))
        pygame.display.flip()

    def set_user_grid(self):
        mx,my = pygame.mouse.get_pos()
        r = round(mx/10-0.5)
        c = round(my/10-0.5)
        self.grids[self.active_grid][c][r] = 1

    def reset_grid(self):
        for c in range(self.num_rows):
            for r in range(self.num_cols):
                self.grids[self.active_grid][c][r] = 0

    def clear_cell(self):
        mx,my = pygame.mouse.get_pos()
        r = round(mx/10-0.5)
        c = round(my/10-0.5)
        self.grids[self.active_grid][c][r] = 0

    def run(self):
        pause = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #chooese a cell
                    if event.button == 1:
                        self.set_user_grid()
                    if event.button == 3:
                        self.clear_cell()
                if event.type == pygame.KEYDOWN:
                    #reset the whole grid
                    if event.unicode == 'r':
                        self.reset_grid()
                    #toggel pause
                    if event.unicode == 'p':
                        if pause == False:
                            pause = True
                        else:
                            pause = False                  
            if pause == False:
                self.update_gen()
            self.draw_grid()
            self.clock.tick(10)
                       
if __name__ == '__main__':
    game = LifeGame()
    game.run()
