from . import project_5_point

class Spots:
    def __init__ (self):
        '''Initializes a new spots object given a list of all center points of a
        board'''

        self._center_list = []
        self._center_colors = []
        

    def center_list(self) -> list:
        '''Returns a list of center points fractional coordinates'''

        return self._center_list

    def spot_color_list(self) -> list:
        '''Returns a list of spot colors corresponding to each center
        point'''

        return self._center_colors

    def countblack(self) -> int:
        '''Returns the number of black spots on the board'''

        Counter = 0
        
        for spots in self._center_colors:

            if spots == 'black':
                Counter += 1

        return Counter


    def countwhite(self) -> int:
        '''Returns the number of white spots on the board'''

        Counter = 0

        for spots in self._center_colors:

            if spots == 'white':
                Counter += 1

        return Counter

    def addspot(self, center_point: tuple, spotcolor:str):
        '''Adds another center point to the center list and
        its color to the color list'''

        self._center_list.append(center_point)
        self._center_colors.append(spotcolor)

    def removespot(self, center_point: tuple):
        '''Removes a center point from the center list and its color
        from the color list'''

        index = self._center_list.index(center_point)

        self._center_list.remove(center_point)
        del self._center_colors[index]

    def construct_gameboard(self, all_center_list: list, colamount: int):
        '''Creates an Othello Game Board that can be used by
        the Othello Logic module given all the center points'''

        game_board = []
        game_board_rows = []

        counter = 0
        
        for index in range(len(all_center_list)):

            counter += 1
            
            if all_center_list[index] in self._center_list:

                color_index = self._center_list.index(all_center_list[index])

                if self._center_colors[color_index] == 'white':
                    game_board_rows.append('W')

                elif self._center_colors[color_index] == 'black':
                    game_board_rows.append('B')

            else:
                game_board_rows.append('.')

            if counter == colamount:
                game_board.append(game_board_rows)
                game_board_rows = []
                counter = 0
                
        return game_board
    

    def store_gameboard(self, game_board: list):
        '''Stores a gameboard the center colors'''

        result = []

        for rows in game_board:
            for pieces in rows:

                if pieces == 'W':
                    result.append('white')
                    
                elif pieces == 'B':
                    result.append('black')
                
        self._center_colors = result
        

    def store_ordered_spots(self):
        '''Reorders the center list to reflect the
        image of a game board'''

        self._center_list = sorted(self._center_list, key= lambda x: (x[1],x[0]))
    
                
    

