from . import project_5_game_logic
from . import project_5_spots_model
from . import project_5_point
import tkinter
from tkinter import messagebox

class OthelloApplication:

    def __init__(self, state: project_5_spots_model.Spots):
        '''Initialzes the Othello GUI Application'''

        self._game_started = False

        self._dummy_root_window = tkinter.Tk()
        self._dummy_root_window.withdraw()

        dialog = OptionDialog()
        dialog.show()

        self._rowamount = dialog.rowamount()
        self._colamount = dialog.colamount()
        self._player_turn = dialog.firstplayer()
        self._win_condition = dialog.wincondition()

        if type(self._rowamount) != int or type(self._colamount) != int or len(self._player_turn) != 1 or len(self._win_condition) != 1:
            return
        
        self._spot_size = 0.02
        self._change_spot_size()
        
        self._disc_color = 'white'

        self._state = state
        
        self._root_window = tkinter.Tk()
        
        self._root_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._version_text = tkinter.Label(master = self._root_window, font = ('Helvetica', 12),
                                           text = 'FULL', foreground = 'red')
        self._version_text.grid(row = 0, column = 1, sticky = tkinter.E + tkinter.N)

        self._switch_text = tkinter.Label(master = self._root_window, font = ('Helvetica', 10),
                                          text = 'Switch Color', foreground = 'blue')
        self._switch_text.grid(row = 1, column = 1, sticky = tkinter.E + tkinter.S)

        self._pregame_placedisc_button = tkinter.Button(master = self._root_window, text = self._disc_color,
                                                        font = ('Helvetica', 20), command = self._switch_disc_color)
        
        self._pregame_placedisc_button.grid(row = 2, column = 1)

        self._done_placing_button = tkinter.Button(master = self._root_window, text = 'Done!',
                                                  font = ('Helvetica', 20), command = self._destroy_pregame_widgets)
        self._done_placing_button.grid(row = 2, column = 0, sticky = tkinter.W)
        
        self._Othello_canvas = tkinter.Canvas(
            master = self._root_window, width = 500, height = 500,
            background = '#cce6ff')

        self._Othello_canvas.grid(
            row = 0, column = 0, padx = 30, pady = 30,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)


        self._Othello_canvas.bind('<Configure>', self.redraw_board)

        self._Othello_canvas.bind('<Button-1>', self.clicked_canvas)
        
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        
    def on_closing(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._root_window.quit()
            
    def run(self):
        '''Runs the Othello Application'''
        
        try:
            self._root_window.mainloop()

        except AttributeError:
            return

    def _destroy_pregame_widgets(self):
        '''Destroys the pre-game widgets'''
        
        self._pregame_placedisc_button.destroy()
        self._switch_text.destroy()
        self._done_placing_button.destroy()

        self._start_game()


    def _start_game(self):
        '''Begins the Othello game'''

        self._game_started = True

        self._black_score = self._state.countblack()
        self._white_score = self._state.countwhite()
        
        self._score_text = tkinter.Label(master = self._root_window, text = 'Score:', font = ('Helvetica', 25))
        self._score_text.grid(row = 1, column = 0, padx = 15, sticky = tkinter.W)


        self._black_score_text = tkinter.Label(master = self._root_window, text = 'Black: ' + str(self._black_score),
                                          font = ('Helvetica', 15))
        self._black_score_text.grid(row = 2, column = 0, padx = 15, sticky = tkinter.W)
        

        self._white_score_text = tkinter.Label(master = self._root_window, text  = 'White: ' + str(self._white_score),
                                          font = ('Helvetica', 15))
        self._white_score_text.grid(row = 3, column = 0, padx = 15, sticky = tkinter.W)


        self._turn_text = tkinter.Label(master = self._root_window, text = 'Turn: ' + self._player_turn,
                                        font = ('Helvetica', 15))
        self._turn_text.grid(row = 5, column = 0, padx = 15, pady = 15, sticky = tkinter.W)


        self._root_window.rowconfigure(4, minsize = 15, weight = 0)

        self._check_gamestate()


    def _game_over(self, GameState: 'GameState'):
        '''Handles the GUI when the Othello game ends'''

        self._Othello_canvas.unbind('<Button-1>')
    
        self._turn_text.destroy()

        winner = GameState.winner(self._win_condition)
        
        if winner == 'WINNER: BLACK':
            self._winner_black = tkinter.Label(master = self._root_window, text = 'Black Wins!',
                                               font = ('Helvetica', 30))
            self._winner_black.grid(row = 4, column = 0, padx = 15, pady = 15, sticky = tkinter.W)

        elif winner == 'WINNER: WHITE':
            self._winner_white = tkinter.Label(master = self._root_window, text = 'White Wins!',
                                               font = ('Helvetica', 30))
            self._winner_white.grid(row = 4, column = 0, padx = 15, pady = 15, sticky = tkinter.W)
            

        elif winner == 'WINNER: NONE':
            self._winner_black = tkinter.Label(master = self._root_window, text = 'Draw!',
                                               font = ('Helvetica', 30))
            self._winner_black.grid(row = 4, column = 0, padx = 15, pady = 15, sticky = tkinter.W)
        

        self._playagain_button = tkinter.Button(master = self._root_window, text = 'Play Again?',
                                                        font = ('Helvetica', 20), command = self._playagain)
        
        self._playagain_button.grid(row = 4, column = 1, padx = 15, pady = 15, sticky = tkinter.E)
        

    def _playagain(self):
        '''Constructs another Othello Application to allow the
        user to play the game again'''

        self._root_window.destroy()

        OthelloApp_again = OthelloApplication(project_5_spots_model.Spots())

        OthelloApp_again.run()

        
    def redraw_board(self, event: tkinter.Event):
        '''Draws the Othello GUI Board'''

        self._Othello_canvas.delete(tkinter.ALL)

        canvas_width = self._Othello_canvas.winfo_width()
        canvas_height = self._Othello_canvas.winfo_height()
        
        for rows in range(1, self._rowamount):
            row_begin_point = project_5_point.from_frac(0, (rows/self._rowamount))
            row_end_point = project_5_point.from_frac(1, (rows/self._rowamount))

            row_begin_x, row_begin_y = row_begin_point.pixel(canvas_width, canvas_height)
            row_end_x, row_end_y  = row_end_point.pixel(canvas_width, canvas_height)

            self._Othello_canvas.create_line(
                row_begin_x, row_begin_y,
                row_end_x, row_end_y,)

        for columns in range(1, self._colamount):
            col_begin_point = project_5_point.from_frac((columns/self._colamount), 0)
            col_end_point = project_5_point.from_frac((columns/self._colamount), 1)

            col_begin_x, col_begin_y = col_begin_point.pixel(canvas_width, canvas_height)
            col_end_x, col_end_y  = col_end_point.pixel(canvas_width, canvas_height)

            self._Othello_canvas.create_line(
                col_begin_x, col_begin_y,
                col_end_x, col_end_y,)

        self.redraw_spots(canvas_width, canvas_height)
        
            
    def redraw_spots(self, canvas_width: int, canvas_height: int):
        '''Redraws the spots on the board'''
            
        for index in range(len(self._state.center_list())):
                
            bounding_box_topleft_point = project_5_point.from_frac((self._state.center_list()[index][0] - self._spot_size), (self._state.center_list()[index][1] - self._spot_size))
            bounding_box_bottomright_point = project_5_point.from_frac((self._state.center_list()[index][0] + self._spot_size), (self._state.center_list()[index][1] + self._spot_size))
                                   
            bounding_box_topleft_x, bounding_box_topleft_y = bounding_box_topleft_point.pixel(canvas_width, canvas_height)
            bounding_box_bottomright_x, bounding_box_bottomright_y = bounding_box_bottomright_point.pixel(canvas_width, canvas_height)
                            
            self._Othello_canvas.create_oval(
                bounding_box_topleft_x, bounding_box_topleft_y,
                bounding_box_bottomright_x, bounding_box_bottomright_y,
                fill = self._state.spot_color_list()[index], outline = '#000000')
                
            
    def clicked_canvas(self, event: tkinter.Event) -> None:
        '''Handles what happens when the board is clicked'''
    
        
        canvas_width = self._Othello_canvas.winfo_width()
        canvas_height = self._Othello_canvas.winfo_height()

        click_point = project_5_point.from_pixel(event.x, event.y,
                                                 canvas_width, canvas_height)
        
        box_center_list = self.boxcenter()

        box_height = self.boxheight_frac()
        box_width = self.boxwidth_frac()

        past_game_board = self._state.construct_gameboard(box_center_list, self._colamount)
               
        for center_fract in box_center_list:

            if (center_fract[0]-(box_width/2)) < click_point.frac()[0] < (center_fract[0] + (box_width/2)) and (center_fract[1]-(box_height/2)) < click_point.frac()[1] < (center_fract[1] + (box_height/2)):

                player_move = self._find_twodim_index(center_fract, box_center_list)
                
                bounding_box_topleft_point = project_5_point.from_frac((center_fract[0] - self._spot_size), (center_fract[1] - self._spot_size))
                bounding_box_bottomright_point = project_5_point.from_frac((center_fract[0] + self._spot_size), (center_fract[1] + self._spot_size))
                           
                bounding_box_topleft_x, bounding_box_topleft_y = bounding_box_topleft_point.pixel(canvas_width, canvas_height)
                bounding_box_bottomright_x, bounding_box_bottomright_y = bounding_box_bottomright_point.pixel(canvas_width, canvas_height)

                if self._game_started:
                    GameState = project_5_game_logic.GameState(past_game_board, self._player_turn)

                    try:
                        condition = GameState.predictmoves(GameState.enemy_turn(), GameState.player_turn())
                        BoardTurnList = GameState.insertpiece(player_move)

                        self._player_turn = BoardTurnList[1]

                        index = player_move[1] + player_move[0] 

                        self._state.addspot(center_fract, self._disc_color)

                        self._state.store_ordered_spots()
                
                        self._Othello_canvas.create_oval(
                            bounding_box_topleft_x, bounding_box_topleft_y,
                            bounding_box_bottomright_x, bounding_box_bottomright_y,
                            fill = self._disc_color, outline = '#000000')

                        self._change_disc_color()

                        self._state.store_gameboard(BoardTurnList[0])

                        self.redraw_board(event)


                        self._black_score_text.config(text = 'Black: ' + str(GameState.countblack()))
                        self._white_score_text.config(text = 'White: ' + str(GameState.countwhite()))
                        self._turn_text.config(text = 'Turn: ' + self._player_turn)

                        check_gamestate = self._check_gamestate()

                        if check_gamestate == 'GameOver':
                            self._game_over(GameState)

                    except project_5_game_logic.InvalidMoveError:
                        pass


                else:
                    if center_fract in self._state.center_list():
                        self._state.removespot(center_fract)
                        self.redraw_board(event)

                    else:
                        self._state.addspot(center_fract, self._disc_color)
                
                        self._Othello_canvas.create_oval(
                            bounding_box_topleft_x, bounding_box_topleft_y,
                            bounding_box_bottomright_x, bounding_box_bottomright_y,
                            fill = self._disc_color, outline = '#000000')
       

        game_board = self._state.construct_gameboard(box_center_list, self._colamount)


    def _check_gamestate(self):
        '''Checks whether or not the game is over or if a turn is skipped'''

        box_center_list = self.boxcenter()
        
        past_game_board = self._state.construct_gameboard(box_center_list, self._colamount)

        GameState = project_5_game_logic.GameState(past_game_board, self._player_turn)

        self._check_skipturn(GameState)

        check_gameover = GameState.gameover()

        if check_gameover == 'GameOver':
            self._game_over(GameState)


    def _check_skipturn(self, GameState: 'GameState'):
        '''Checks whether or not to skip a player's turn'''
        
        enemy_turn = GameState.enemy_turn()
        player_turn = GameState.player_turn()
        
        check_skipturn = GameState.predictmoves(enemy_turn, player_turn)
     
        if type(check_skipturn) == tuple:
            self._player_turn = check_skipturn[1]
            self._turn_text.config(text = 'Turn: ' + self._player_turn)


    def _find_twodim_index(self, center_fract: float, box_center_list: list) -> list:
        '''Finds the corresponding 2d list index of a center
        fraction in a list of center fractions'''

        result = []

        center_index = box_center_list.index(center_fract)

        for rows in range(0, self._rowamount):
            twodim_index = center_index - (self._colamount * rows)
    
            if twodim_index >= 0:
                result = []
                result.append(rows)
                result.append(twodim_index)

        return result

           
    def boxheight_frac(self) -> float:
        '''Determines the fractional height of every box on the board'''

        box_height_fract = (2/self._rowamount) - (1/self._rowamount)

        return box_height_fract


    def boxwidth_frac(self) -> float:
        '''Determines the fractional width of every box on the board'''

        box_width_fract = (2/self._colamount) - (1/self._colamount)

        return box_width_fract


    def boxcenter(self) -> float:
        '''Determines the fractional center of every box on the board'''

        row_center_list = []
        col_center_list = []
        box_center_fract_list = []
        
        for rows in range(1, self._rowamount*2, 2):
            row_center_point = (rows/(self._rowamount*2))
            row_center_list.append(row_center_point)

        for columns in range(1, self._colamount*2, 2):
            col_center_point = (columns/(self._colamount*2))
            col_center_list.append(col_center_point)

        for row_point in row_center_list:
            for col_point in col_center_list:
                box_center_fract_list.append((col_point, row_point))

        return box_center_fract_list

    def _switch_disc_color(self):
        '''Switches the color of the disc'''
    
        if self._disc_color == 'white':
            self._disc_color = 'black'
            self._pregame_placedisc_button['text'] = 'black'

        elif self._disc_color == 'black':
            self._disc_color = 'white'
            self._pregame_placedisc_button['text'] = 'white'


    def _change_spot_size(self):
        '''Changes the spot size of the disc based
        on the board size'''

        if self._rowamount <= 8 and self._colamount <= 8:
            self._spot_size = 0.04

        if self._rowamount <= 6 and self._colamount <= 6:
            self._spot_size = 0.06

        if self._rowamount == 4 and self._colamount == 4:
            self._spot_size = 0.08

    def _change_disc_color(self):
        '''Changes the color of the disc based on
        who's turn it is'''

        if self._player_turn == 'B':
            self._disc_color = 'black'

        elif self._player_turn == 'W':
            self._disc_color = 'white'
                          

class OptionDialog:

    def __init__(self):

        self._dialog_window = tkinter.Toplevel()

        self._header_text = tkinter.Label(master = self._dialog_window, font = ('Helvetica', 20),
                                          text = 'Game Config', foreground = 'black')
        self._header_text.grid(row = 0, column = 0, padx = 20, pady = 20,
                               sticky = tkinter.N + tkinter.W)
                                          

        self._row_text = tkinter.Label(master = self._dialog_window, font = ('Helvetica', 12),
                                           text = 'Select \n Row Amount:', foreground = 'red')
        self._row_text.grid(row = 4, column = 0, padx = 15, sticky = tkinter.E)


        self._col_text = tkinter.Label(master = self._dialog_window, font = ('Helvetica', 12),
                                           text = 'Select \n Column Amount:', foreground = 'blue')
        self._col_text.grid(row = 4, column = 3, padx = 15, sticky = tkinter.E)


        self._firstplayer_text = tkinter.Label(master = self._dialog_window, font = ('Helvetica', 12),
                                           text = 'Select \n First Player:', foreground = 'green')
        self._firstplayer_text.grid(row = 4, column = 6, padx = 15, sticky = tkinter.E)


        self._win_text = tkinter.Label(master = self._dialog_window, font = ('Helvetica', 12),
                                           text = 'Select \n Win Condition:', foreground = 'purple')
        self._win_text.grid(row = 4, column = 9, padx = 15, sticky = tkinter.E)

        
        self._RowtkIntVar = tkinter.IntVar()

        self._rows_button4 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '4 rows', variable = self._RowtkIntVar,
                                                 value = 4)

        self._rows_button6 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '6 rows', variable = self._RowtkIntVar,
                                                 value = 6)

        self._rows_button8 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '8 rows', variable = self._RowtkIntVar,
                                                 value = 8)

        self._rows_button10 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '10 rows', variable = self._RowtkIntVar,
                                                  value = 10)

        self._rows_button12 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '12 rows', variable = self._RowtkIntVar,
                                                  value = 12)

        self._rows_button14 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '14 rows', variable = self._RowtkIntVar,
                                                  value = 14)

        self._rows_button16 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '16 rows', variable = self._RowtkIntVar,
                                                  value = 16)

        
        self._rows_button4.grid(row = 1, column = 1)
        self._rows_button6.grid(row = 2, column = 1)
        self._rows_button8.grid(row = 3, column = 1)
        self._rows_button10.grid(row = 4, column = 1)
        self._rows_button12.grid(row = 5, column = 1)
        self._rows_button14.grid(row = 6, column = 1)
        self._rows_button16.grid(row = 7, column = 1)
        


        self._ColtkIntVar = tkinter.IntVar()

        self._cols_button4 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '4 columns', variable = self._ColtkIntVar,
                                                 value = 4)

        self._cols_button6 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '6 columns', variable = self._ColtkIntVar,
                                                 value = 6)

        self._cols_button8 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '8 columns', variable = self._ColtkIntVar,
                                                 value = 8)

        self._cols_button10 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '10 columns', variable = self._ColtkIntVar,
                                                  value = 10)

        self._cols_button12 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '12 columns', variable = self._ColtkIntVar,
                                                  value = 12)

        self._cols_button14 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '14 columns', variable = self._ColtkIntVar,
                                                  value = 14)

        self._cols_button16 = tkinter.Radiobutton(master = self._dialog_window,
                                    text = '16 columns', variable = self._ColtkIntVar,
                                                  value = 16)



        self._cols_button4.grid(row = 1, column = 4)
        self._cols_button6.grid(row = 2, column = 4)
        self._cols_button8.grid(row = 3, column = 4)
        self._cols_button10.grid(row = 4, column = 4)
        self._cols_button12.grid(row = 5, column = 4)
        self._cols_button14.grid(row = 6, column = 4)
        self._cols_button16.grid(row = 7, column = 4)
        


        self._PlayerIntVar = tkinter.IntVar()

        self._Black_button = tkinter.Radiobutton(master = self._dialog_window,
                                                 text = 'Black', variable = self._PlayerIntVar,
                                                 value = 1)

        self._White_button = tkinter.Radiobutton(master = self._dialog_window,
                                                 text = 'White', variable = self._PlayerIntVar,
                                                 value = 2)

        self._Black_button.grid(row = 3, column = 7)
        self._White_button.grid(row = 5, column = 7)




        self._WinIntVar = tkinter.IntVar()

        self._Least_button = tkinter.Radiobutton(master = self._dialog_window,
                                                 text = 'Least Discs', variable = self._WinIntVar,
                                                 value = 1)

        self._Most_button = tkinter.Radiobutton(master = self._dialog_window,
                                                 text = 'Most Discs', variable = self._WinIntVar,
                                                 value = 2)

        self._Least_button.grid(row = 3, column = 10, padx = (0,15), sticky = tkinter.W)
        self._Most_button.grid(row = 5, column = 10, padx = (0,15), sticky = tkinter.W)
        
        self._dialog_window.columnconfigure(2, minsize = 30, weight = 1)
        self._dialog_window.columnconfigure(5, minsize = 30, weight = 1)
        self._dialog_window.columnconfigure(8, minsize = 30, weight = 1)
        self._dialog_window.rowconfigure(8, weight = 1)
        

        self._done_button = tkinter.Button(master = self._dialog_window,
                                           text = 'Done!', font = ('Helvetica', 20),
                                           command = self._command_clicked)
        self._done_button.grid(row = 8, column = 10, padx = 15, pady = 15, sticky = tkinter.S + tkinter.E)

        self._row_amount = ''
        self._col_amount = ''
        self._first_player = ''
        self._win_condition = ''

    def show(self) -> None:

        self._dialog_window.grab_set()
        self._dialog_window.wait_window()


    def _command_clicked(self):
        
        self._row_amount = self._RowtkIntVar.get()
        self._col_amount = self._ColtkIntVar.get()
        self._first_player = self._PlayerIntVar.get()
        self._win_condition = self._WinIntVar.get()

        if self._row_amount != 0 and self._col_amount != 0 and self._first_player != 0 and self._win_condition != 0:
            self._dialog_window.destroy()


    def rowamount(self):

        return self._row_amount


    def colamount(self):

        return self._col_amount


    def firstplayer(self):

        if self._first_player == 1:
            return 'B'

        elif self._first_player == 2:
            return 'W'


    def wincondition(self):

        if self._win_condition == 1:
            return '<'

        elif self._win_condition == 2:
            return '>'
        

        
if __name__ == '__main__':

    OthelloApp = OthelloApplication(project_5_spots_model.Spots())

    OthelloApp.run()

    
