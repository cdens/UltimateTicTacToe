#!/usr/bin/env python3
#Ultimate tic-tac-toe implementation with PyGame

import pygame, tictactoe, time, logging


class TicTacToeGame:
    
    def __init__(self):
        pygame.init()
        
        #game hasn't started, no valid player selected
        self.player = 0
        self.game_happening = False
        self.active_board = False

        #set width/height constants for window and generate it
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        
        #create ultimate tic tac toe object to track game
        self.game = tictactoe.UltimateBoard()
        
        #define coordinaes for boards and squares, draw board
        self.set_constants()
        self.draw_board()
        
        #create marker for active board (won't appear until first turn is taken)
        self.active_marker = ActiveBoardMarker(self.screen, self.main_board, self.SQMARKERHOFFSET, self.SQMARKERVOFFSET, self.LWID_BIG, [self.X_COLOR,self.O_COLOR]) 
                
        #start the game
        self.run()
        
        
    def set_constants(self):
        #set dimensions for game region
        self.GAME_WIDTH = int(14/15*self.SCREEN_WIDTH)
        self.GAME_HEIGHT = int(14/15*self.SCREEN_HEIGHT)
        self.GAME_H_START = int(1/30*self.SCREEN_WIDTH)
        self.GAME_V_START = int(1/30*self.SCREEN_HEIGHT)
        
        #colors for board components
        self.LINE_COLOR = (217, 219, 217) #lines
        self.LWID_BIG = 6
        self.LWID_SMALL = 3
        self.BG_COLOR = (64, 66, 63) #background
        self.X_COLOR = (166, 60, 60) # X (red)
        self.O_COLOR = (60, 60, 179) #O (blue)
        self.SQ_COLOR = (60,170,60) #active board marker (green)
        
        self.SQUARE_W_OFFSET = int(1/20*self.SCREEN_WIDTH) #dimensions of the large squares
        self.SQUARE_V_OFFSET = int(1/20*self.SCREEN_HEIGHT)
        self.BIG_SQUARE_WIDTH = int(1/3*self.GAME_WIDTH - 2*self.SQUARE_W_OFFSET)
        self.BIG_SQUARE_HEIGHT = int(1/3*self.GAME_HEIGHT - 2*self.SQUARE_V_OFFSET)
        
        self.SMALL_SQUARE_WIDTH = int(1/3*self.BIG_SQUARE_WIDTH) #dimensions of the small squares
        self.SMALL_SQUARE_HEIGHT = int(1/3*self.BIG_SQUARE_HEIGHT)
        
        self.CHAR_W_OFFSET = int(1/40*self.SCREEN_WIDTH) #dimensions for x and o
        self.CHAR_V_OFFSET = int(1/40*self.SCREEN_HEIGHT)
        
        self.SQMARKERHOFFSET = int(1/50*self.SCREEN_WIDTH)#offset for active board marker inside large board
        self.SQMARKERVOFFSET = int(1/50*self.SCREEN_HEIGHT)
        
        
    def draw_board(self):
        
        # Fill the background with dark gray
        self.screen.fill(self.BG_COLOR)
        
        self.main_board = BoardDimensions(self.GAME_H_START,self.GAME_V_START,self.GAME_WIDTH,self.GAME_HEIGHT)
        self.draw_board_lines(self.main_board,self.LWID_BIG,self.LINE_COLOR)
        
        self.small_boards = [[],[],[]]
        for i in range(3):
            for j in range(3):
                self.small_boards[i].append(BoardDimensions(self.main_board.x[i]+self.SQUARE_W_OFFSET, self.main_board.y[j]+self.SQUARE_V_OFFSET, self.BIG_SQUARE_WIDTH, self.BIG_SQUARE_HEIGHT))
                self.draw_board_lines(self.small_boards[i][j],self.LWID_SMALL,self.LINE_COLOR)
                
        #adding characters
        for i in range(3):
            for j in range(3):
                
                for ii in range(3):
                    for jj in range(3):
                        board_status, square_status = self.game.return_status([i,j],[ii,jj])
                        if square_status:
                            self.add_character([i,j],[ii,jj],square_status)
                if board_status:
                    self.set_board_won([i,j], board_status)
                        
        pygame.display.flip()
        
        
        
    def draw_board_lines(self,b,lwid,color): #bounding_box ~ [xstart,ystart,width,height]
        lines = [[(b.x[1],b.y[0]),(b.x[1],b.y[3])], 
                    [(b.x[2],b.y[0]),(b.x[2],b.y[3])], 
                    [(b.x[0],b.y[1]),(b.x[3],b.y[1])], 
                    [(b.x[0],b.y[2]),(b.x[3],b.y[2])]]
        
        for line in lines:
            pygame.draw.line(self.screen, color, line[0], line[1], width=lwid)
        pygame.display.flip() #update display
    
    
    def set_board_won(self,board,player):
        if player == 1:
            color = self.X_COLOR
        elif player == 2:
            color = self.O_COLOR
        self.draw_board_lines(self.small_boards[board[0]][board[1]], self.LWID_SMALL, color)
        #self.add_character(False,board,player)
    
        
    #draw character within coordinates for box    
    def add_character(self,cboard,csquare,player):
        #get bounds for box
        if cboard: #cboard is a list giving coordinates for specific square
            lwid = self.LWID_SMALL
            cb = self.small_boards[cboard[0]][cboard[1]]
        else: #cboard = False, therefore draw a character over entire board indicated by csquare
            lwid = self.LWID_BIG
            cb = self.main_board
            
        if player == 1: #draw X
            b = [cb.x[csquare[0]],cb.x[csquare[0]+1],cb.y[csquare[1]],cb.y[csquare[1]+1]] #[xs,xe,ys,ye]
            pygame.draw.line(self.screen,self.X_COLOR,(b[0],b[2]),(b[1],b[3]),width=lwid)
            pygame.draw.line(self.screen,self.X_COLOR,(b[0],b[3]),(b[1],b[2]),width=lwid)
        elif player == 2: #draw O
            crect = pygame.Rect(cb.x[csquare[0]], cb.y[csquare[1]], int(1/3*cb.width), int(1/3*cb.height))
            pygame.draw.ellipse(self.screen,self.O_COLOR,crect,width=lwid)
        pygame.display.flip() #update display
        
    
    #identifies whether a mouse click was within a valid square, if so triggers take_turn function
    def identify_click_point(self,pos,player):
                
        #identify whether a valid box was selected
        #if active_board = False, then the user can select anywhere, otherwise active_board = [i,j] indices for current board
        if self.active_board:
            irange = [self.active_board[0]]
            jrange = [self.active_board[1]]
        else:
            irange = range(3)
            jrange = range(3)
                    
        for i in irange: #i and j are for the large boxes
            for j in jrange:
                cb = self.small_boards[i][j]
                
                for ii in range(3): #ii and jj are for the squares within each box
                    for jj in range(3): 
                        if (cb.x[ii] < pos[0] < cb.x[ii+1]) and (cb.y[jj] < pos[1] < cb.y[jj+1]):
                            self.take_turn([i,j],[ii,jj],player)
                            return True

        return False #if point wasn't within a valid range, return false
        
    
    def take_turn(self,cboard,csquare,player):
        move_success, board_won, game_won, win_possible, active_board = self.game.take_turn(player,cboard,csquare)
        logging.debug(f"player {player} move on board {cboard} square {csquare}, turn/board/game = {move_success}/{board_won}/{game_won}, new board={active_board} ")
        
        if move_success: #add character to selected square
            self.active_board = active_board
            self.add_character(cboard,csquare,player)
            
            if board_won: #mark that board was won by player
                self.set_board_won(cboard,player)
            
            if game_won: #declare game winner
                self.declare_winner(player)
            elif not win_possible: #draw
                self.declare_winner(3)
            else: #allow other player to make selection
                self.switch_active_player()
                self.draw_board()
                newplayer = 1 if player == 2 else 2
                self.active_marker.draw(active_board,newplayer)                
            
            
        
    def switch_active_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1
        
        
            
    def declare_winner(self,player):
        self.game_happening = False 
        playerchar = ["x","o"]
        if player == 1:
            color = self.X_COLOR
        elif player == 2:
            color = self.O_COLOR
        elif player == 3:
            color = self.SQ_COLOR
        logging.info(f"Game won by player {playerchar[player-1]}")
        self.draw_board_lines(self.main_board, self.LWID_BIG, color)
            
    
    def run(self):
    
        # Run until the user asks to quit or game is over
        running = True
        self.game_happening = True
        self.player = 1
        self.active_board = False
        
        while running:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #user clicked exit
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP and self.game_happening: #user clicked something else (square?)
                    pos = pygame.mouse.get_pos() #pos = position (y,x) tuple in pixels
                    self.identify_click_point(pos, self.player)
    
        pygame.quit() #loop exits when player clicks window close button so kill pygame instance/stop running
    

        
        
class BoardDimensions:
    
    def __init__(self,xs,ys,width,height):
        
        self.width = width
        self.height = height
        self.x = [xs,int(xs + 1/3*width),int(xs + 2/3*width),xs + width]
        self.y = [ys,int(ys + 1/3*height),int(ys + 2/3*height),ys + height]
        
        boxlimits = [[],[],[]] #format for each bounding box is x1,x2,y1,y2
        for i in range(3):
            for j in range(3):
                boxlimits[i].append([self.x[i],self.x[i+1],self.y[j],self.y[j+1]])
        

                
    
class ActiveBoardMarker:
    
    def __init__(self,screen,board_dimensions,hoffset,voffset,lwid,colors):
        
        self.image = screen        
        self.bd = board_dimensions
        self.hoffset = hoffset
        self.voffset = voffset
        self.colors = colors
        self.lwid = lwid
        
    def draw(self,cboard,newplayer):
        
        color = self.colors[newplayer-1]
        
        xL = self.bd.x[cboard[0]] + self.hoffset #left X
        xR = self.bd.x[cboard[0]+1] - self.hoffset #right X
        yB = self.bd.y[cboard[1]] + self.voffset #bottom Y
        yT = self.bd.y[cboard[1]+1] - self.voffset #top Y
        
        cbd = [(xL,yB),(xL,yT),(xR,yT),(xR,yB)] #four corners of lines (bottom left, top left, top right, bottom right)
        
        #args = screen,color,(x1,y1),(x2,y2)
        pygame.draw.line(self.image,color,cbd[0],cbd[1],width=self.lwid) #left side
        pygame.draw.line(self.image,color,cbd[1],cbd[2],width=self.lwid) #top
        pygame.draw.line(self.image,color,cbd[2],cbd[3],width=self.lwid) #right side
        pygame.draw.line(self.image,color,cbd[3],cbd[0],width=self.lwid) #bottom
        pygame.display.flip() #update display
        
        
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    game = TicTacToeGame() #create and run a game instance
    
    
    