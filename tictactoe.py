#! /usr/bin/env python3
# tictactoe.py
# logic for playing ultimate tic tac toe game


#individual tic-tac-toe square **has option for attached board for ultimate tic-tac-toe
class Square:
    
    def __init__(self):
        self._status = 0
        self.board = None #can set this to a Board object if it's a square in an ultimate board
        
    def get_status(self):
        return self._status
        
    def set_status(self,status,override=False): #won't let you change status on a square that's already been set
        if self._status and not override:
            return False
        else:
            self._status = status
            return True
            


#tic-tac-toe board
class Board:
    
    def __init__(self):
        #initialize squares on board
        self.squares = [[],[],[]]
        for i in range(3):
            for j in range(3):
                self.squares[i].append(Square())
                
        self._status = 0
        self.last_player = 0
        self.win_options = initialize_win_options()
        self.win_type = []
        self.win_possible = [True, True]
        
                
    def set_square(self,coords,player):
        
        option = 0
        result = self.squares[coords[0]][coords[1]].set_status(player) #returns true if square set
        if result:
            won_game = self.check_win(player,False)
            self.win_possible[player-1] = self.check_win(player,True)
            if won_game:
                result = 2
                
            self.check_board_full()
            
        return result
        
    def get_board_status(self):
        return self._status
        
    def check_win(self,player,possible): #possible=True checks to see if a win is possible for the player
                
        for option in self.win_options:
            num_set = 0
            for coord in option:
                cstatus = self.squares[coord[0]][coord[1]].get_status()
                if cstatus == player or (possible and cstatus == 0):
                    num_set += 1
            if num_set == 3: #3 in a row, it's a win (not possible means it's checking for actual wins)
                if not possible:
                    self.win_type = option
                    self._status = player
                return True
        
        return False #nothing was 3 in a row, not a win
        
    def check_board_full(self): #checks if board is full, resets if necessary
        sum_occupied = 0
        for row in self.squares:
            for square in row:
                if square.get_status():
                    sum_occupied += 1
        if sum_occupied == 9:
            for row in self.squares:
                for square in row:
                    square.set_status(0,override=True) #override normal function to prevent changing status back to 0
    
                    
                    
                    
                    
                    

#ultimate tic-tac-toe board with sub-boards in each square
class UltimateBoard(Board):
    
    def __init__(self):
        
        super().__init__() #create Board instance
        
        #create sub-board for each square
        for i in range(3):
            for j in range(3):
                self.squares[i][j].board = Board()
                
                
    def return_status(self,board,square):
        return self.squares[board[0]][board[1]].board.get_board_status(), self.squares[board[0]][board[1]].board.squares[square[0]][square[1]].get_status()
                
                
    def take_turn(self,player,board,square):
        
        move_success = False
        game_won = False
        board_won = False
        new_board = board
        win_possible = True
        
        if self.last_player == 0 or (self.last_player == 1 and player == 2) or (self.last_player == 2 and player == 1):
            result = self.squares[board[0]][board[1]].board.set_square(square,player)
            if result:
                move_success = True
                self.last_player = player
                new_board = square #next player has to move on board defined by selected square
                if result == 2: #square's board was won
                    self.squares[board[0]][board[1]].set_status(player) #update status for that square
                    board_won = True
                    game_won = self.check_win(player, False) #check to see if the overall game has been won
                    win_possible = self.check_win(player, True) #check to see if the overall game can be won
        
        return move_success, board_won, game_won, win_possible, new_board
        
        
        
        
def initialize_win_options():
    win_options = []
    
    #straight across or down
    for i in range(3):
        win_options.append([(i,j) for j in range(3)]) #down
        win_options.append([(j,i) for j in range(3)]) #across
        
    #diagonal wins
    win_options.append([(i,i) for i in range(3)])
    win_options.append([(i,2-i) for i in range(3)])
        
    return win_options   
    
        
        
        
        
        
        
        
        
        
        
        