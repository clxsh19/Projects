import pygame
import numpy as np
import sys
from piece import King, Pawn, Knight, Linear_piece, King
from piece import check_for_check
class Chess():

    def __init__(self):

        self.size = 80
        self.board_colors = [(230,200,200), (140,80,80)]
        # self.board = np.array([['bR','bN','bB','bQ','bK','bB','bN','bR'],
        #                        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        #                        ['--','--','--','--','--','--','--','--'],
        #                        ['--','--','--','--','--','--','--','--'],
        #                        ['--','--','--','--','--','--','--','--'],
        #                        ['--','--','--','--','--','--','--','--'],
        #                        ['wP','wP','wP','wP','wP','wP','wP','wP'],
        #                        ['wR','wN','wB','wQ','wK','wB','wN','wR']
        #                        ])
        self.board = np.array([['bR','bN','--','bQ','bK','bB','--','bR'],
                               ['bP','bP','--','bP','--','bP','--','bP'],
                               ['--','--','--','--','--','--','--','--'],
                               ['--','--','--','--','--','--','--','--'],
                               ['--','--','--','--','wN','--','--','--'],
                               ['--','bB','--','wP','--','--','--','--'],
                               ['wP','wP','--','--','wP','wP','--','wP'],
                               ['wR','--','--','--','wK','--','--','wR']
                               ])

        self.selected_piece_loc = ()
        self.current_player = 'w'
        # 0 index for white, 1 for black
        self.check = [False,False]
        self.castle = [[True,True],[True,True]]
        self.player1 = 'w'
        self.player2 = 'b'

    def load_images(self):
        images = {}
        pieces = ['bR','bN','bB','bQ','bK','bP','wR','wN','wB','wQ','wK','wP']

        for piece in pieces:
            images[piece] = pygame.transform.smoothscale(pygame.image.load('imgs\\%s.png'%(piece)),(70,70))

        return images

    def draw_pieces(self, screen, images):
        screen_x = 40
        screen_y = 40

        for row in range(8):
            for col in range(8):
                piece_name = self.board[row][col]
                
                if piece_name != '--':
                    img = images[piece_name]
                    piece_rect = img.get_rect(center=(screen_x,screen_y))
                    screen.blit(img, piece_rect)

                screen_x += 80
            screen_x = 40
            screen_y += 80
        
        pygame.display.update()

    def draw_board(self, screen):
        screen_x = 0
        screen_y = 0

        for row in range(8):
            for col in range(8):
                if (row,col) == self.selected_piece_loc:
                    pygame.draw.rect(screen, (30,230,30), (screen_x ,screen_y , self.size-1 , self.size-1))
                else:
                    pygame.draw.rect(screen, self.board_colors[(row+col)%2], (screen_x ,screen_y , self.size-1 , self.size-1))

                screen_x += self.size
            screen_x = 0
            screen_y += self.size

        pygame.display.update()

    def get_move(self, selected_sq_loc):
        enemy_color = "w" if self.current_player == "b" else "b"

        # else:
        # if a peice is selected, check the peice and get its valid move
        if self.selected_piece_loc:
            current_king = self.current_player+'K'
            king_loc = np.where(self.board == current_king)

            selected_peices = {'P':Pawn(self.board, king_loc), 'N':Knight(self.board, king_loc), 'B':Linear_piece(self.board, king_loc), 'R':Linear_piece(self.board, king_loc), 'Q':Linear_piece(self.board, king_loc), 'K':King(self.board, self.check, self.castle)}
            Linear_peices = ('R', 'B', 'Q')
            Other_peices = ('P', 'N', 'K')

            # if queen, rook or bishop
            if self.board[self.selected_piece_loc][1] in Linear_peices:

                linear_peice = Linear_piece(self.board, king_loc)
                # Bishop
                if self.board[self.selected_piece_loc][1] == 'B':
                    valid_moves = linear_peice.get_bishop_moves(self.selected_piece_loc)

                # Rook
                elif self.board[self.selected_piece_loc][1] == 'R':
                    valid_moves = linear_peice.get_rook_moves(self.selected_piece_loc)

                # Queen
                elif self.board[self.selected_piece_loc][1] == 'Q':
                    valid_moves = linear_peice.get_queen_moves(self.selected_piece_loc)

                # if the selected square is in valid moves or
                # if selected another peice of same color to change selected peice
                if selected_sq_loc in valid_moves or self.board[selected_sq_loc][0] == self.board[self.selected_piece_loc][0]:
                        self.make_move(selected_sq_loc)

            # other peices
            elif self.board[self.selected_piece_loc][1] in Other_peices:
                # intiating the peice class
                peice = selected_peices[self.board[self.selected_piece_loc][1]]
                # getting the valid moves
                valid_moves = peice.get_valid_moves(self.selected_piece_loc)
                # if the selected square is in valid moves or
                # if selected another peice of same color
                if selected_sq_loc in valid_moves or self.board[selected_sq_loc][0] == self.board[self.selected_piece_loc][0]:
                        self.make_move(selected_sq_loc)

        # no peice is selected so select one
        else:
            if self.board[selected_sq_loc][0] == self.current_player:
                self.make_move(selected_sq_loc)


    def make_move(self, selected_sq_loc):

        king_n = 0 if self.current_player == "w" else 1

        # if there is no selected piece then select the selected sq if it's a peice
        if not self.selected_piece_loc:
            if self.board[selected_sq_loc] != '--':
                self.selected_piece_loc = selected_sq_loc

        # if a peice is selected
        elif self.selected_piece_loc:
            if self.board[self.selected_piece_loc][0] == self.current_player:
                if self.board[selected_sq_loc][0] != self.current_player:

                    #if rook moves king looses that side castle right
                    if self.board[self.selected_piece_loc][1] == 'R':
                        # white rook
                        if self.board[self.selected_piece_loc][0] == 'w':
                            # left side rook moved
                            if self.selected_piece_loc[1] == 0:
                                self.castle[0][0] = False
                            # right side rook moved
                            elif self.selected_piece_loc[1] == 7:
                                self.castle[0][1] = False

                        # black rook
                        if self.board[self.selected_piece_loc][0] == 'b':
                            # left side rook moved
                            if self.selected_piece_loc[1] == 0:
                                self.castle[1][0] = False
                            # right side rook moved
                            elif self.selected_piece_loc[1] == 7:
                                self.castle[1][1] = False
                    
                     # castle move
                    if self.board[self.selected_piece_loc][1] == 'K':
                        if self.check[king_n] == False:
                            # if king has left side castle right
                            if self.castle[king_n][0] == True:
                                # selected move is the left side castle move
                                if selected_sq_loc == (self.selected_piece_loc[0],2):
                                    self.board[self.selected_piece_loc[0],3] = self.current_player+'R'
                                    self.board[self.selected_piece_loc[0],0] = '--'
                            # right side
                            if self.castle[king_n][1] == True:
                                if selected_sq_loc == (self.selected_piece_loc[0],6):
                                    self.board[self.selected_piece_loc[0],5] = self.current_player+'R'
                                    self.board[self.selected_piece_loc[0],7] = '--'
                            self.board[selected_sq_loc] = self.board[self.selected_piece_loc]
                            self.board[self.selected_piece_loc] = '--'

                        else:
                            self.board[selected_sq_loc] = self.board[self.selected_piece_loc]
                            self.board[self.selected_piece_loc] = '--'
                            

                        # king moved so it looses it's right to castle
                        self.castle[king_n][0] = False
                        self.castle[king_n][1] = False

                    # making move
                    if self.board[self.selected_piece_loc][1] != 'K' and self.board[self.selected_piece_loc] != '--':
                        self.board[selected_sq_loc] = self.board[self.selected_piece_loc]
                        self.board[self.selected_piece_loc] = '--'
                    # removing selected piece
                    self.selected_piece_loc=()

                    # change current player
                    if self.current_player == 'w':
                        self.current_player = 'b'
                    else:
                        self.current_player = 'w'

                    #check for check
                    current_king = self.current_player+'K'
                    king_loc = np.where(self.board == current_king)
                    row, col = king_loc[0][0], king_loc[1][0]
                    self.check = check_for_check(self.current_player, self.board, self.check, row, col)
                    # print(self.check)
                    # print()

                else:
                    if self.board[selected_sq_loc][0] != '--':
                        self.selected_piece_loc = selected_sq_loc

    def main(self):
        pygame.init()
        # screen size
        BOARD_SIZE = WIDTH,HEIGHT = 640,640
        screen = pygame.display.set_mode(BOARD_SIZE)
        clock = pygame.time.Clock()
        images = self.load_images()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #select a piece
                    if event.button == 1:
                        x,y = pygame.mouse.get_pos()
                        col = round(x/80-0.5)
                        row = round(y/80-0.5)
                        selected_sq_loc = (row,col)
                        
                        self.get_move(selected_sq_loc)
                            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_board(screen)
            self.draw_pieces(screen, images)
            clock.tick(10)

chess = Chess()
chess.main()

