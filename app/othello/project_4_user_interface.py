from . import project_4_game_logic

print('FULL')


##Main User Interface

def run_user_interface():
    '''Runs the user interface'''

    row_amount = specify_dimension_amount()

    column_amount = specify_dimension_amount()

    first_player = pick_first_player()

    win_condition = pick_win_condition()

    board = read_board_contents(row_amount, column_amount)

    track_game(board, first_player, win_condition)



##User Interface Display    
    
def display_game(GameState: 'GameState', win_condition: str) -> None:
    '''Displays the board on the console'''
    
    black_amount = GameState.countblack()

    white_amount = GameState.countwhite()

    print('B: ' + str(black_amount) + '  ' + 'W: ' + str(white_amount))

    print_board(GameState)
    
    game_over = GameState.gameover()
    
    if game_over == 'GameOver':
        
        winner = GameState.winner(win_condition)
        print(winner)
        return winner
    
    else:
        print('TURN: ' + GameState.player_turn())
        return 'No Winner'


def print_board(GameState: 'GameState') -> None:
    '''Prints out a board'''

    for row in GameState.board():
        row = ' '.join(row)
        print(row)
        


##Game Managers
    
def update_gamestate(new_board: list, player_turn: str) -> 'GameState':
    '''Updates the gamestate'''

    GameState = project_4_game_logic.GameState(new_board, player_turn)

    return GameState


def track_game(board: list, turn: str, win_condition: str) -> '???':
    '''Tracks the current state of the game'''
    
    GameState = update_gamestate(board, turn)
    
    state = display_game(GameState, win_condition)
    
    if state == 'Winner':
        
        return None

    elif state == 'No Winner':
    
        BoardTurnList = ask_move(GameState)
        
        if BoardTurnList == 'GameOver':
            winner = GameState.winner(win_condition)
            print(winner)
            
            return None
        
        else:
            track_game(BoardTurnList[0], BoardTurnList[1], win_condition)



##User Input Handlers
    
def specify_dimension_amount():
    '''Takes a valid number of rows as input and returns it'''
    
    while True:
        
        try:
            dimension_amount = int(input().strip())
            
            if dimension_amount >= 4 and dimension_amount <= 16:
                if dimension_amount%2 == 0:
                    return dimension_amount

                else:
                    print('That\'s not an even number')
            else:
                print('That\'s not a number between 4 and 16')
        except:
            print('That\'s not a number.')


def pick_first_player():
    '''Takes B/W as input and returns it'''

    while True:

        first_player = input().strip()

        if first_player == 'B' or first_player == 'W':
            return first_player

        else:
            print('That\'s not a valid choice.')


def pick_win_condition():
    '''Takes >/< as input and returns it'''

    while True:

        win_condition = input().strip()

        if win_condition == '>' or win_condition == '<':
            return win_condition

        else:
            print('That\'s not a valid choice.')


def read_board_contents(row_amount: int, column_amount: int) -> list:
    '''Reads the contents of a board as input'''

    board = []

    for num in range(row_amount):
        
        row = input().strip()

        row = row[:(column_amount*2)-1]

        board.append(row.split())
 
    return board


def ask_move(GameState: 'GameState') -> 'GameState':
    '''Takes a valid player move as input and returns a GameState'''

    while True:
        
        game_over = GameState.gameover()

        if game_over == 'GameOver':
            return 'GameOver'
        
        result = []
                
        player_move = input().strip()

        if ' ' in player_move:
            RowCol_List = player_move.split()

            for RowCol in RowCol_List:

                try:
                    result.append(int(RowCol)-1)

                except ValueError:
                    print('INVALID')
            
            try:
                BoardTurnList = GameState.insertpiece(result)
                print('VALID')
                return BoardTurnList

            except project_4_game_logic.InvalidMoveError:
                print('INVALID')

            except project_4_game_logic.InvalidRowColError:
                print('INVALID')
                
            except project_4_game_logic.GameOverError:
                print('INVALID')
            

        else:
            print('INVALID')
     

if __name__ == '__main__':
    run_user_interface()