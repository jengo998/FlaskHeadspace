import copy

class GameState:
    def __init__(self, board: list, turn: str):
        '''Initializes the GameState to have a board and turn'''
        self._board = board
        self._turn = turn


    ##Access Attribute Methods
        
    def player_turn(self) -> str:
        '''Specifies the player's turn'''

        return self._turn

    def enemy_turn(self) -> str:
        '''Specifies the enemy turn'''
        
        if self._turn == 'B':
            return 'W'

        elif self._turn == 'W':
            return 'B'
        
    def board(self):
        '''Returns the board'''

        return self._board



    ##Board Detail Methods
    
    def rownum(self) -> int:
        '''Returns the number of rows in the board'''

        return len(self._board)

    def colnum(self) -> int:
        '''Returns the number of columns in the board'''

        for columns in self._board:
            return len(columns)

    def identify(self, player_move: list):
        '''Identifies a disc on the grid'''

        try:
            if self._board[player_move[0]][player_move[1]] == '.':
                return '.'

            if self._board[player_move[0]][player_move[1]] == 'B':
                return 'B'
            
            if self._board[player_move[0]][player_move[1]] == 'W':
                return 'W'

        except:
            raise InvalidRowColError

        

    ##Game Condition Manager Methods
        
    def gameover(self):
        '''Determines whether the game is over'''
        
        empty_amount = self.countempty()

        if empty_amount == 0:
            return 'GameOver'
        
        elif self.predictmoves(self.enemy_turn(), self.player_turn()) == 'GameOver':
            return 'GameOver'

        elif self.countblack() == 0:
            return 'GameOver'

        elif self.countwhite() == 0:
            return 'GameOver'

        else:
            return 'None'

    def winner(self, win_condition: str):
        '''Determines who the winner is given a win condition'''

        black_amount = self.countblack()
        white_amount = self.countwhite()
            
        if win_condition == '>':

            if black_amount > white_amount:
                return 'WINNER: BLACK'

            elif white_amount > black_amount:
                return 'WINNER: WHITE'

            elif white_amount == black_amount:
                return 'WINNER: NONE'

        elif win_condition == '<':
            
            if black_amount < white_amount:
                return 'WINNER: BLACK'

            elif white_amount < black_amount:
                return 'WINNER: WHITE'

            elif white_amount == black_amount:
                return 'WINNER: NONE'


    
    ##Board Updater Methods
            
    def insertpiece(self, player_move: list) -> tuple:
        '''Makes a valid move given a list of a row and a column'''
        
        piece = self.identify(player_move)

        if piece == 'B' or piece == 'W':
            raise InvalidMoveError

        else:

            condition = self.gameover()

            if condition == 'GameOver':
                raise GameOverError

            else:
                    
                if self._turn == 'B':
                    self._board = self.makemove(player_move, self.enemy_turn(), self._turn)
                    self._board[player_move[0]][player_move[1]] = 'B'
                    self._turn = 'W'
                    return self._board, self._turn


                elif self._turn == 'W':
                    self._board = self.makemove(player_move, self.enemy_turn(), self._turn)
                    self._board[player_move[0]][player_move[1]] = 'W'
                    self._turn = 'B'
                    return self._board, self._turn


    def makemove(self, player_move: list, enemy_turn: str, player_turn: str) -> list:
        '''Checks whether the move is valid in correspondence
        with the rules of Othello and flips the enemy pieces'''
    
        temp1 = _create_temp_board(self._board)
        temp2 = _create_temp_board(self._board)
           
        try:
            temp2 = _makemove_left(temp2, player_move, enemy_turn, player_turn)
            
        except IndexError:
            pass
                    
                
        try:
            temp2 = _makemove_right(temp2, player_move, enemy_turn, player_turn, self.colnum())
                    
        except IndexError:
            pass
        

        try:
            temp2 = _makemove_up(temp2, player_move, enemy_turn, player_turn)
                    
        except IndexError:
            pass
        

        try:
            temp2 = _makemove_down(temp2, player_move, enemy_turn, player_turn, self.rownum())

        except IndexError:
            pass
                
                
        try:
            diagonal_distance = self.diagtopleft(player_move)
            temp2 = _makemove_topleft(temp2, player_move, enemy_turn, player_turn, diagonal_distance)
                      
        except IndexError:
            pass


        try:
            diagonal_distance = self.diagbottomright(player_move)
            temp2 = _makemove_bottomright(temp2, player_move, enemy_turn, player_turn, diagonal_distance)
                                
        except IndexError:
            pass
                                                        
                    

        try:
            diagonal_distance = self.diagtopright(player_move)
            temp2 = _makemove_topright(temp2, player_move, enemy_turn, player_turn, diagonal_distance)

        except IndexError:
            pass


        try:
            diagonal_distance = self.diagbottomleft(player_move)
            temp2 = _makemove_bottomleft(temp2, player_move, enemy_turn, player_turn, diagonal_distance)
            
        except IndexError:
            pass


        if temp1 == temp2:
            raise InvalidMoveError

        return temp2


                
    ##Piece Countering Methods
            
    def countblack(self):
        '''Counts the amount of black pieces in a board'''

        counter = 0

        for row in self._board:

            for column in row:

                if column == 'B':
                    counter += 1

        return counter

    def countwhite(self):
        '''Counts the amount of white pieces in a board'''

        counter = 0

        for row in self._board:

            for column in row:

                if column == 'W':
                    counter += 1

        return counter

    def countempty(self):
        '''Counts the amount of empty pieces in a board'''

        counter = 0

        for row in self._board:

            for column in row:

                if column == '.':
                    counter += 1

        return counter

    

    ##Diagonal Measuring Methods

    def diagtopleft(self, player_move: list):
        '''Returns how long the top-left diagonal is given a point'''

        row_distance = player_move[0] 

        column_distance = player_move[1]

        if row_distance < column_distance:
            diagonal_distance = row_distance

        elif column_distance < row_distance:
            diagonal_distance = column_distance

        elif column_distance == row_distance:
            diagonal_distance = row_distance
        
        return diagonal_distance
    

    def diagbottomleft(self, player_move: list):
        '''Returns how long the bottom-left diagonal is given a point'''

        row_distance = player_move[0] 

        column_distance = player_move[1]

        if row_distance > column_distance:
            diagonal_distance = row_distance

        elif column_distance > row_distance:
            diagonal_distance = column_distance

        elif column_distance == row_distance:
            diagonal_distance = row_distance

        return diagonal_distance 
        

    def diagtopright(self, player_move: list):
        '''Returns how long the top-right diagonal is given a point'''

        row_distance = player_move[0]

        column_distance = player_move[1]

        if row_distance > column_distance:
            diagonal_distance = row_distance

        elif column_distance > row_distance:
            diagonal_distance = column_distance

        elif column_distance == row_distance:
            diagonal_distance = row_distance
        
        return diagonal_distance
    

    def diagbottomright(self, player_move: list):
        '''Returns how long the bottom-right diagonal is given a point'''

        row_distance = self.rownum() - player_move[0]

        column_distance = self.colnum() - player_move[1]
    
        if row_distance < column_distance:
            diagonal_distance = row_distance

        elif column_distance < row_distance:
            diagonal_distance = column_distance

        elif column_distance == row_distance:
            diagonal_distance = row_distance
        
        return diagonal_distance 
    


    ##Game Predictor Method
    
    def predictmoves(self, enemy_turn: str, player_turn: str):
        '''Predicts all the possible player moves, switching the turn to the
        opposite player if no move is available, or ends the game if neither
        player is able to make a move'''

        result = 'No possible moves'
        
        possible_moves = _identify_empty_index(self._board)

        for player_move in possible_moves:
            
            try:
                board = self.makemove(player_move, enemy_turn, player_turn)
    
                if type(board) == list:
                    result = 'Possible moves'
                    return result

            except InvalidMoveError:
                pass
    
        if result == 'No possible moves':
            
            try:
                board = self.makemove(player_move, enemy_turn, player_turn)

            except:
                
                for enemy_player_move in possible_moves:

                    try:
                        board = self.makemove(enemy_player_move, player_turn, enemy_turn)
                        self._turn = self.enemy_turn()
                        return self._board, self._turn
                    
                    except InvalidMoveError:
                        pass

        
            return 'GameOver'


       

#####################
##Exception Classes##
#####################

class InvalidRowColError(Exception):
    '''Raised when a non-existent row or column is given'''
    pass


class InvalidMoveError(Exception):
    '''Raised when an invalid move is given'''
    pass

class GameOverError(Exception):
    '''Raised when a move is trying to be made after
    the game is over'''
    pass




########################
##Enemy Piece Checkers##
########################

def _check_enemy_row(enemy_turn: str, player_turn: str, board: list, begin_piece: int,
                     common_index: int, end_piece: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in a row
    and returns the index of those consecutive enemy pieces'''
    
    result = []
    
    for enemy_piece in range(begin_piece, end_piece):
        
        if board[common_index][enemy_piece] == enemy_turn:
            
            result.append(enemy_piece)

        elif board[common_index][enemy_piece] == player_turn:
            
            result = []
            result.extend(_check_enemy_row(enemy_turn, player_turn, board, enemy_piece+1, common_index, end_piece))
            
        elif board[common_index][enemy_piece] == '.':
            result = []
            return result
        
    return result

    
def _check_enemy_column(enemy_turn: str, player_turn: str, board: list, begin_piece: int,
                        common_index: int, end_piece: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in a column
    and returns the index of those consecutive enemy pieces'''

    result = []
    
    for enemy_piece in range(begin_piece, end_piece):
        if board[enemy_piece][common_index] == enemy_turn:
            result.append(enemy_piece)

        elif board[enemy_piece][common_index] == player_turn:
            result = []
            result.extend(_check_enemy_column(enemy_turn, player_turn, board, enemy_piece+1, common_index, end_piece))
            
        elif board[enemy_piece][common_index] == '.':
            result = []
            return result
            
    return result


def _check_enemy_topleft_diagonal(enemy_turn: str, player_turn: str, board: list, begin_row_piece: int,
                                  begin_col_piece: int, player_move: list, diagonal_distance: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in
    a top-left diagonal and returns the index of those consecutive
    enemy pieces'''

    result = []
    
    enemy_row = []
    enemy_col = []
    
    for enemy_row_span in range(begin_row_piece, player_move[0]):
        enemy_row.append(enemy_row_span)
        
    for enemy_col_span in range(begin_col_piece, player_move[1]):
        enemy_col.append(enemy_col_span)
   
    for index in range(len(enemy_row)-1, 0, -1):
        
        enemyindex = []

        if board[enemy_row[index]][enemy_col[index]] == enemy_turn:
                                            
            enemyindex.append(enemy_row[index])
            enemyindex.append(enemy_col[index])
        
            result.append(enemyindex)

        elif board[enemy_row[index]][enemy_col[index]] == '.':
            result = []
            return result

        elif board[enemy_row[index]][enemy_col[index]] == player_turn:
            return result

    return result


def _check_enemy_bottomright_diagonal(enemy_turn: str, player_turn: str, board: list, end_row_piece: int,
                                      end_col_piece: int, player_move: list, diagonal_distance: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in
    a bottom-right diagonal and returns the index of those consecutive
    enemy pieces'''

    result = []
    
    enemy_row = []
    enemy_col = []

    for enemy_row_span in range(player_move[0]+1, end_row_piece):
        
        enemy_row.append(enemy_row_span)
           
    for enemy_col_span in range(player_move[1]+1, end_col_piece):
        
        enemy_col.append(enemy_col_span)

    for index in range(len(enemy_row)):
    
        enemyindex = []
        
        if board[enemy_row[index]][enemy_col[index]] == enemy_turn:
                                            
            enemyindex.append(enemy_row[index])
            enemyindex.append(enemy_col[index])
            
            result.append(enemyindex)

        elif board[enemy_row[index]][enemy_col[index]] == '.':
            result = []
            return result
        
        elif board[enemy_row[index]][enemy_col[index]] == player_turn:
            return result


    return result
    

def _check_enemy_topright_diagonal(enemy_turn: str, player_turn: str, board: list, end_row_piece: int,
                                   end_col_piece: int, player_move: list, diagonal_distance: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in
    a top-right diagonal and returns the index of those consecutive
    enemy pieces'''  
    
    result = []
    
    enemy_row = []
    enemy_col = []
    
    for enemy_row_span in range(player_move[0]-1, end_row_piece, -1):
        
        enemy_row.append(enemy_row_span)
           
    for enemy_col_span in range(player_move[1]+1, end_col_piece):
        
        enemy_col.append(enemy_col_span)
   
    for index in range(len(enemy_row)):

        enemyindex = []
        
        if board[enemy_row[index]][enemy_col[index]] == enemy_turn:
                                            
            enemyindex.append(enemy_row[index])
            enemyindex.append(enemy_col[index])
            
            result.append(enemyindex)

        elif board[enemy_row[index]][enemy_col[index]] == '.':
            result = []
            return result
            
        elif board[enemy_row[index]][enemy_col[index]] == player_turn:
            return result
        
    return result
    
    
def _check_enemy_bottomleft_diagonal(enemy_turn: str, player_turn: str, board: list, end_row_piece: int,
                                     end_col_piece: int, player_move: list, diagonal_distance: int) -> list:
    '''Checks whether enemy pieces are between 2 player pieces in
    a bottom-left diagonal and returns the index of those consecutive
    enemy pieces'''

    result = []
    
    enemy_row = []
    enemy_col = []

    for enemy_row_span in range(player_move[0]+1, end_row_piece):
        
        enemy_row.append(enemy_row_span)
           
    for enemy_col_span in range(player_move[1]-1, end_col_piece, -1):
        
        enemy_col.append(enemy_col_span)
    
    for index in range(len(enemy_row)):
        
        enemyindex = []
        
        if board[enemy_row[index]][enemy_col[index]] == enemy_turn:
                                            
            enemyindex.append(enemy_row[index])
            enemyindex.append(enemy_col[index])
            
            result.append(enemyindex)   

        elif board[enemy_row[index]][enemy_col[index]] == '.':
            result = []
            return result
        
        elif board[enemy_row[index]][enemy_col[index]] == player_turn:
            return result

    
        
    return result



########################
##Enemy Piece Flippers##
########################

def _makemove_left(board: list, player_move: list, enemy_turn: str, player_turn: str) -> list:
    '''Flips enemy pieces to the left if the move is legal'''

    player_span = player_move[1]

    for piece in range(player_span):
        
        if board[player_move[0]][(player_move[1]-1)] == enemy_turn:
           
            if board[player_move[0]][piece] == player_turn:
                
                enemy_pieces = _check_enemy_row(enemy_turn, player_turn, board,
                                                piece+1, player_move[0], (player_move[1]))
          
                for enemy_piece in enemy_pieces:
                    board[player_move[0]][enemy_piece] = player_turn

    return board              


def _makemove_right(board: list, player_move: list, enemy_turn: str, player_turn: str, colnum: int) -> list:
    '''Flips enemy pieces to the right if the move is legal'''
    
    for piece in range(player_move[1], colnum):
                
        if board[(player_move[0])][(player_move[1]+1)] == enemy_turn:
            if board[player_move[0]][piece] == player_turn:

                enemy_pieces = _check_enemy_row(enemy_turn, player_turn, board,
                                                player_move[1]+1, player_move[0], piece)
                
                for enemy_piece in enemy_pieces:
                    board[player_move[0]][enemy_piece] = player_turn

    return board


def _makemove_up(board: list, player_move: list, enemy_turn: str, player_turn: str) -> list:
    '''Flips enemy pieces upwards if the move is legal'''
    
    player_span = player_move[0]
    
    for piece in range(player_span):

        if board[(player_move[0]-1)][(player_move[1])] == enemy_turn:
            if board[piece][player_move[1]] == player_turn:
               
                enemy_pieces = _check_enemy_column(enemy_turn, player_turn, board, piece+1,
                                                   player_move[1], player_move[0])
            
                for enemy_piece in enemy_pieces:
                    board[enemy_piece][player_move[1]] = player_turn

    return board


def _makemove_down(board: list, player_move: list, enemy_turn: str, player_turn: str, rownum: int) -> list:
    '''Flips enemy pieces downwards if the move is legal'''
    
    for piece in range(player_move[0], rownum):
        
        if board[(player_move[0]+1)][(player_move[1])] == enemy_turn:
            if board[piece][player_move[1]] == player_turn:
                
                enemy_pieces = _check_enemy_column(enemy_turn, player_turn, board,
                                                   player_move[0]+1, player_move[1], piece)
                
                for enemy_piece in enemy_pieces:
                    board[enemy_piece][player_move[1]] = player_turn
                    
    return board


def _makemove_topleft(board: list, player_move: list, enemy_turn: str, player_turn: str, diagonal_distance: int) -> list:
    '''Flips enemy pieces to the topleft if the move is legal'''

    if (player_move[1] - 1) < 0:
        raise IndexError
    
    if board[(player_move[0]-1)][(player_move[1]-1)] == enemy_turn:

        for index in range(1, diagonal_distance+1):
                   
            if board[player_move[0] - index][player_move[1] - index] == player_turn:
                       
                begin_row_piece = player_move[0] - index
                begin_col_piece = player_move[1] - index
                        
                enemy_pieces = _check_enemy_topleft_diagonal(enemy_turn, player_turn, board,
                                                begin_row_piece, begin_col_piece, player_move, diagonal_distance)
                        
                for enemy_piece in enemy_pieces:
                        board[enemy_piece[0]][enemy_piece[1]] = player_turn

    return board


def _makemove_bottomright(board: list, player_move: list, enemy_turn: str, player_turn: str, diagonal_distance: tuple) -> list:
    '''Flips enemy pieces to the bottomright if the move is legal'''
    
    if board[(player_move[0]+1)][(player_move[1]+1)] == enemy_turn:
        
        for index in range(1, diagonal_distance+1):
           
            if board[player_move[0]+index][player_move[1]+index] == player_turn:
                    
                end_row_piece = player_move[0] + index
                end_col_piece = player_move[1] + index

                enemy_pieces = _check_enemy_bottomright_diagonal(enemy_turn, player_turn, board,
                                                    end_row_piece, end_col_piece, player_move, diagonal_distance)
                
                
                for enemy_piece in enemy_pieces:
                    board[enemy_piece[0]][enemy_piece[1]] = player_turn
                    
    return board


def _makemove_topright(board: list, player_move: list, enemy_turn: str, player_turn: str, diagonal_distance: int) -> list:
    '''Flips enemy pieces to the topright if the move is legal'''
    
    if board[(player_move[0]-1)][(player_move[1]+1)] == enemy_turn:

        for index in range(1, diagonal_distance+1):
            
            if board[player_move[0] - index][player_move[1] + index] == player_turn:
                        
                end_row_piece = player_move[0] - index
                end_col_piece = player_move[1] + index
                        
                enemy_pieces = _check_enemy_topright_diagonal(enemy_turn, player_turn, board,
                                                        end_row_piece, end_col_piece, player_move, diagonal_distance)
                
                for enemy_piece in enemy_pieces:
                    board[enemy_piece[0]][enemy_piece[1]] = player_turn

    return board


def _makemove_bottomleft(board: list, player_move: list, enemy_turn: str, player_turn: str, diagonal_distance: tuple) -> list:
    '''Flips enemy pieces to the bottomleft if the move is legal'''

    if (player_move[1] - 1) < 0:
        raise IndexError
    
    if board[(player_move[0]+1)][(player_move[1]-1)] == enemy_turn:
        
        for index in range(1, diagonal_distance+1):
            
            if board[player_move[0]+index][player_move[1]-index] == player_turn:
                
                end_row_piece = player_move[0] + index
                end_col_piece = player_move[1] - index
                        
                enemy_pieces = _check_enemy_bottomleft_diagonal(enemy_turn, player_turn, board,
                                                        end_row_piece, end_col_piece, player_move, diagonal_distance)
                
                for enemy_piece in enemy_pieces:
                    board[enemy_piece[0]][enemy_piece[1]] = player_turn
    
    return board

###############
##Misc. Tools##
###############

def _create_temp_board(board: list) -> list:
    '''Creates a copy of a board and returns it'''
    
    result = copy.deepcopy(board)

    return result


def _identify_empty_index(board: list) -> list:
    '''Gives the index of every empty piece on
    a board'''

    result = [(ix,iy) for ix, row in enumerate(board) for iy, i in enumerate(row) if i == '.']

    return result
