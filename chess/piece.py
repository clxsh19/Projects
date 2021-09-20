
# [ ['bR','bN','bB','bQ','bK','bB','bN','bR'],
#   ['bP','bP','bP','bP','bP','bP','bP','bP'],
#   ['--','--','--','--','--','--','--','--'],
#   ['--','--','--','--','--','--','--','--'],
#   ['--','--','--','--','--','--','--','--'],
#   ['--','--','--','--','--','--','--','--'],
#   ['wP','wP','wP','wP','wP','wP','wP','wP'],
#   ['wR','wN','wB','wQ','wK','wB','wN','wR'] ]



def check_for_check(current_player, board, check, row, col):
        check = [False,False]
        enemy_color = "w" if current_player == "b" else "b"
        checking_peices = 0

        # checking diagonally
        diagonall_directions = ((-1,-1), (-1,1), (1,-1), (1,1))

        for d in diagonall_directions:
            if checking_peices < 1:
                for i in range(1,8):
                    m_row = row + d[0] * i
                    m_col = col + d[1] * i

                    if 0 <= m_row <=7 and 0 <= m_col <=7:
                    
                        # if a opposite color peice in path
                        if board[m_row][m_col][0] == enemy_color:
                            # checking for enemy pawn in forward directions
                            if i == 1 and d in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                                if board[m_row][m_col][1] == 'P' and board[m_row][m_col][0] == enemy_color:
                                    if current_player == 'w':
                                        check[0] = True
                                    else:
                                        check[1] = True
                                    checking_peices +=1
                                    break

                            # bishop and queen can check diagonally 
                            if board[m_row][m_col][1] == 'B' or board[m_row][m_col][1] == 'Q':
                                if current_player == 'w':
                                    check[0] = True
                                else:
                                    check[1] = True
                                checking_peices +=1
                                break
                            else:
                                break
                        # elif ally piece
                        elif board[m_row][m_col][0] == current_player:
                            break

        # checking up, down, left and right
        linear_directions = ((-1,0), (1,0), (0,-1), (0,1))

        for d in linear_directions:
            if checking_peices < 1:
                for i in range(1,8):
                    m_row = row + d[0] * i
                    m_col = col + d[1] * i

                    if 0 <= m_row <=7 and 0 <= m_col <=7:
                        # if a opposite color peice in path
                        if board[m_row][m_col][0] == enemy_color:
                            # only queen and rook can check in straight
                            if board[m_row][m_col][1] == 'R' or board[m_row][m_col][1] == 'Q':
                                if current_player == 'w':
                                    check[0] = True
                                else:
                                    check[1] = True
                                checking_peices += 1
                                break
                            # other black peice cant check so stop looking in this direction
                            else:
                                break

                        # elif ally piece
                        elif board[m_row][m_col][0] == current_player:
                            break


        #checking for knight checks
        knight_directions = ((-2,-1), (-2,1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2))

        for m in knight_directions:
            if checking_peices < 1:
                m_row = row + m[0]
                m_col = col + m[1]

                if 0 <= m_row <=7 and 0 <= m_col <=7:
                    if board[m_row][m_col][0] == enemy_color:
                        # if it's a knight
                        if board[m_row][m_col][1] == 'N':
                            if current_player == 'w':
                                check[0] = True
                            else:
                                check[1] = True
                            checking_peices +=1
                            break
                        else:
                            break

        return check

class Pawn:

    def __init__(self, board, king_loc):
        self.board = board
        self.king_loc = king_loc

    def get_valid_moves(self, pawn_cords):
        row = pawn_cords[0]
        col = pawn_cords[1]
        moves = []
        king_n = 0 if self.board[row,col][0] == "w" else 1

        if self.board[pawn_cords][0] == 'w':
            # front move if square above is free
            if self.board[row-1][col] == '--':
                if row == 6:
                    moves.append((row-1, col))
                    if self.board[row-2][col] == '--':
                        moves.append((row-2,col))
                else:
                    moves.append((row-1, col))

            # left diagonall capture
            if col != 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append((row-1,col-1))

            # right diagnoall capture
            if col != 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append((row-1, col+1))

        elif self.board[pawn_cords][0] == 'b':
            # front move if square above is free
            if self.board[row+1][col] == '--':
                if row == 1:
                    moves.append((row+1, col))
                    if self.board[row+2][col] == '--':
                        moves.append((row+2,col))
                else:
                    moves.append((row+1, col))

            # left diagonall capture
            if col != 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append((row+1, col-1))

            # right diagnoall capture
            if col != 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append((row+1, col+1))

        right_moves = []
        self.check = [False,False]
        for move in moves:
            row_c, col_c = move[0], move[1]
            board_copy = self.board.copy()
            board_copy[row_c][col_c] = board_copy[row][col]
            board_copy[row][col] = '--'
            
            self.check = check_for_check(self.board[row,col][0], board_copy, self.check, self.king_loc[0][0], self.king_loc[1][0])
            # print(self.check)
            if self.check[king_n] == False:
                right_moves.append((row_c,col_c))

        return right_moves

class Knight:

    def __init__(self, board, king_loc):
        self.board = board
        self.king_loc = king_loc

    def get_valid_moves(self, knight_cords):
        row = knight_cords[0]
        col = knight_cords[1]
        moves = []
        king_n = 0 if self.board[row,col][0] == "w" else 1
        all_moves = ((-2,-1), (-2,1), (2,-1), (2,1), (-1,-2), (-1,2), (1,-2), (1,2))

        for m in all_moves:
            m_row = row + m[0]
            m_col = col + m[1]

            if 0 <= m_row <=7 and 0 <= m_col <=7:
                if self.board[m_row][m_col][0] != self.board[row][col][0]:
                    moves.append((m_row,m_col))

        right_moves = []
        self.check = [False,False]
        for move in moves:
            row_c, col_c = move[0], move[1]
            board_copy = self.board.copy()
            board_copy[row_c][col_c] = board_copy[row][col]
            board_copy[row][col] = '--'
            
            self.check = check_for_check(self.board[row,col][0], board_copy, self.check, self.king_loc[0][0], self.king_loc[1][0])
            if self.check[king_n] == False:
                right_moves.append((row_c,col_c))
    
        return right_moves

class Linear_piece:

    def __init__(self, board, king_loc):
        self.board = board
        self.king_loc = king_loc

    def get_bishop_moves(self, cords):
        row = cords[0]
        col = cords[1]
        moves = []
        king_n = 0 if self.board[row,col][0] == "w" else 1
        direction = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemy_color = "w" if self.board[row][col][0] == "b" else "b"

        for d in direction:
            for i in range(1,8):
                m_row = row + d[0] * i
                m_col = col + d[1] * i

                if 0 <= m_row <=7 and 0 <= m_col <=7:
                    # if a opposite color peice in path
                    if self.board[m_row][m_col][0] == enemy_color:
                        moves.append((m_row,m_col))
                        break
                    # if empty space
                    elif self.board[m_row][m_col] == '--':
                        moves.append((m_row,m_col))
                    else:
                        break      
                else:
                    break

        right_moves = []
        self.check = [False,False]
        for move in moves:
            row_c, col_c = move[0], move[1]
            board_copy = self.board.copy()
            board_copy[row_c][col_c] = board_copy[row][col]
            board_copy[row][col] = '--'
            
            self.check = check_for_check(self.board[row,col][0], board_copy, self.check, self.king_loc[0][0], self.king_loc[1][0])
            if self.check[king_n] == False:
                right_moves.append((row_c,col_c))
        
        return right_moves

    def get_rook_moves(self, cords):
        row = cords[0]
        col = cords[1]
        moves = []
        king_n = 0 if self.board[row,col][0] == "w" else 1
        direction = ((-1,0), (1,0), (0,-1), (0,1))
        enemy_color = "w" if self.board[row][col][0] == "b" else "b"

        for d in direction:
            for i in range(1,8):
                m_row = row + d[0] * i
                m_col = col + d[1] * i

                if 0 <= m_row <=7 and 0 <= m_col <=7:
                    # if a opposite color peice in path
                    if self.board[m_row][m_col][0] == enemy_color:
                        moves.append((m_row,m_col))
                        break
                    # if empty space
                    elif self.board[m_row][m_col] == '--':
                        moves.append((m_row,m_col))
                    else:
                        break      
                else:
                    break

        right_moves = []
        self.check = [False,False]
        for move in moves:
            row_c, col_c = move[0], move[1]
            board_copy = self.board.copy()
            board_copy[row_c][col_c] = board_copy[row][col]
            board_copy[row][col] = '--'
            
            self.check = check_for_check(self.board[row,col][0], board_copy, self.check, self.king_loc[0][0], self.king_loc[1][0])
            if self.check[king_n] == False:
                right_moves.append((row_c,col_c))
        
        return right_moves

    def get_queen_moves(self, cords):
        moves = []

        straight_moves = self.get_rook_moves(cords)
        diagonal_moves = self.get_bishop_moves(cords)

        moves = straight_moves + diagonal_moves

        return moves

class King:

    def __init__(self, board, check, castle):
        self.board = board.copy()
        self.check = check
        self.castle = castle
        self.direction = ((-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1))

    def check_castling(self, cords, castle, king_n, player_color):
        row, col = cords[0], cords[1]
        castle_directions = ((0,-1),(0,1))
        can_castle = [[True,True],[True,True]]
        self.board[row][col] = '--'
        print(castle[king_n][1])

        # left side
        if castle[king_n][0] == True:
            for i in range(1,5):
                c_row = row + castle_directions[0][0] * i
                c_col = col + castle_directions[0][1] * i

                check = check_for_check(player_color, self.board, self.check, c_row, c_col)

                if 0 <= c_row <=7 and 0 <= c_col <=7:
                    if i < 4:    
                        if self.board[c_row,c_col] != '--' or check[king_n] == True:
                            can_castle[king_n][0] = False

                    elif i == 4:
                        if self.board[c_row,c_col][1] != 'R':
                            can_castle[king_n][0] = False

        if castle[king_n][1] == True:
            
            # right side
            for i in range(1,4):
                c_row = row + castle_directions[1][0] * i
                c_col = col + castle_directions[1][1] * i

                check = check_for_check(player_color, self.board, self.check, c_row, c_col)

                if 0 <= c_row <=7 and 0 <= c_col <=7:
                    if i < 3:
                        if self.board[c_row,c_col] != '--' or check[king_n] == True:
                            can_castle[king_n][1] = False

                    elif i == 3:
                        if self.board[c_row,c_col][1] != 'R':
                            can_castle[king_n][1] = False
        
        return can_castle


    def get_valid_moves(self, cords):
        
        row, col = cords[0], cords[1]
        moves = []
        player_color = self.board[row][col][0]
        enemy_color = "w" if player_color == "b" else "b"
        king_n = 0 if player_color == "w" else 1

        self.board[row][col] = '--'
        self.check = check_for_check(player_color, self.board, self.check, row, col)

        for d in self.direction:
            m_row = row + d[0]
            m_col = col + d[1]

            if 0 <= m_row <=7 and 0 <= m_col <=7:
                # if a opposite color peice in path  
                if self.board[m_row][m_col][0] == enemy_color:
                    self.check_new = check_for_check(player_color, self.board, self.check, m_row, m_col)
                    if self.check_new[king_n] == False:
                        moves.append((m_row,m_col))

                # if empty space
                elif self.board[m_row][m_col] == '--':
                    self.check_new = check_for_check(player_color, self.board, self.check, m_row, m_col)
                    if self.check_new[king_n] == False:
                        moves.append((m_row,m_col))

        if self.check[king_n] == False:
            if self.castle[king_n][0] == True or self.castle[king_n][1] == True:
                can_castle = self.check_castling(cords, self.castle, king_n, player_color)
                print(can_castle)
                if can_castle[king_n][0] == True:
                    moves.append((row,2))
                if can_castle[king_n][1] == True:
                    moves.append((row,6))
        print(moves)

        return moves




