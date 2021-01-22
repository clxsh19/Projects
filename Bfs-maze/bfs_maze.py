# BFS algorith for maze solving visulization using pygame

import pygame
import sys
from collections import deque


BOARD_SIZE = WIDTH,HEIGHT = 600, 600
OBSTACLE = "1"
EXIT = "E"
VISITED = "V"
PATH ="P"


class Maze:

    def __init__(self,maze):
        self.maze = maze 
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        # divide by number of rows and cols
        self.box_size = [(WIDTH//14),
                         (HEIGHT//14)]
        # deque
        self.frontier = deque()
        # dict for back routing
        self.solution = {}
        self.clock = pygame.time.Clock()

    def drawMaze(self):
        screen_x = 0
        screen_y = 0
        for row in self.maze:
            for col in row:
                if col == OBSTACLE:              
                    pygame.draw.rect( self.screen,(100,100,100),(screen_x ,screen_y ,self.box_size[0]-1 ,self.box_size[1]-1) )
                if col == '0':
                    pygame.draw.rect( self.screen,(0,150,120),(screen_x ,screen_y ,self.box_size[0] ,self.box_size[1]),1 )
                if col == "S":
                    pygame.draw.rect( self.screen,(255,0,0),(screen_x ,screen_y ,self.box_size[0] ,self.box_size[1]) )
                if col == "E":
                    pygame.draw.rect( self.screen,(255,255,255),(screen_x ,screen_y ,self.box_size[0] ,self.box_size[1]) )
                if col == VISITED:
                    pygame.draw.rect( self.screen,(0,0,255),(screen_x ,screen_y ,self.box_size[0] ,self.box_size[1]) )
                if col == PATH:
                    pygame.draw.rect( self.screen,(0,255,0),(screen_x ,screen_y ,self.box_size[0]-1 ,self.box_size[1]-1) )

                screen_x += self.box_size[0]
            screen_x = 0
            screen_y += self.box_size[1]
        pygame.display.update()

    def search_maze(self, endRow, endCol ,startRow, startCol): 
        self.frontier.append([startRow,startCol])
        # keeps searching while dequeu is not empty
        while len(self.frontier) > 0:
            self.drawMaze()
            # remove from left and put x,y equal to it
            x,y = self.frontier.popleft()

            # checking the top
            if self.maze[x-1][y] != OBSTACLE and self.maze[x-1][y] != VISITED and self.maze[x-1][y] != EXIT:
                # adding to the solution dict for back route
                self.solution[x-1,y] = x,y
                # adding to the deque
                self.frontier.append([x-1,y])
                # marking as visited
                self.maze[x-1][y] = VISITED
            
            # checking the bottom
            if self.maze[x+1][y] != OBSTACLE and self.maze[x+1][y] != VISITED and self.maze[x+1][y] != EXIT:
                self.solution[x+1,y] = x,y
                self.frontier.append([x+1,y])
                self.maze[x+1][y] = VISITED

            # checking the right
            if self.maze[x][y+1] != OBSTACLE and self.maze[x][y+1] != VISITED and self.maze[x][y+1] != EXIT:
                self.solution[x,y+1] = x,y
                self.frontier.append([x,y+1])
                self.maze[x][y+1] = VISITED

            # checking the left
            if self.maze[x][y-1] != OBSTACLE and self.maze[x][y-1] != VISITED and self.maze[x][y-1] != EXIT:
                self.solution[x,y-1] = x,y
                self.frontier.append([x,y-1])
                self.maze[x][y-1] = VISITED
            
            self.handle_events()
            self.clock.tick(30)

        # back tracks after the loop ends
        self.back_route(endRow ,endCol , startRow, startCol)
        return True

    def back_route(self, x, y, startRow, startCol):
        # x,y(end cords)
        while(x,y) != (startRow,startCol):
            # mark x,y as PATH
            self.maze[x][y] = PATH
            # get x,y key value from solution dict
            # and put x,y equal to the keyvalue to keep
            # repeating till x,y == start cords
            x,y = self.solution[x,y]

            # draw the back route as it happens
            self.drawMaze()
            self.handle_events()
            self.clock.tick(10)
        # putting ends cords as "p" last
        self.maze[startRow][startCol] = PATH
 
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main(mazeGrid):
    pygame.init()
    maze = Maze(mazeGrid)
    # to get row and col nums  
    rowNum, colNum = 0,0

    # find the start cords and end cords
    for row in mazeGrid:
        rowNum += 1
        for col in row:
            colNum += 1
            if col == "S":
                # start cordinates
                startRow = rowNum-1
                startCol = colNum-1

            if col == EXIT:
                # end cordinates
                endRow = rowNum-1
                endCol = colNum-2
        colNum = 0
    
    found = False
    while True:
        # runs the search_maze once 
        if found == False:
            found = maze.search_maze(endRow , endCol ,startRow ,startCol)
        maze.drawMaze()
        maze.handle_events()

mazeGrid = [ ['1','S','1','1','1','1','1','1','1','1','1','1','1','1'],
             ['1','0','0','0','0','0','0','0','0','0','0','1','1','1'],
             ['1','0','1','0','0','0','0','0','0','1','0','1','0','1'],
             ['1','0','0','0','1','0','1','1','1','1','0','1','0','1'],
             ['1','1','1','0','1','0','0','0','0','1','0','1','0','E'],
             ['1','1','0','0','0','0','0','0','0','0','0','1','0','1'],
             ['1','0','0','1','1','1','0','1','0','1','0','0','0','1'],
             ['1','1','0','1','0','0','0','1','0','0','0','0','1','1'],
             ['1','1','0','1','0','0','1','0','0','0','1','0','0','1'],
             ['1','0','0','0','1','1','0','1','0','0','1','1','0','1'],
             ['1','0','1','0','0','0','0','1','0','0','0','0','0','1'],
             ['1','1','0','1','1','0','1','0','0','1','1','0','1','1'],
             ['1','1','0','0','0','0','0','0','0','0','1','0','0','1'],
             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1'] ]

# run
if __name__ == '__main__':
    main(mazeGrid)
