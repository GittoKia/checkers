from tkinter import *

class CheckerSquare(Canvas):
    '''displays a square in Checkers'''
    
    def __init__(self,master,color,coord):
        '''CheckerSquare(master,color,coord)
        creates a new color Reversi square at coord'''
        
        # create square
        Canvas.__init__(self,master,width=50,height=50,bg=color,borderwidth=0,highlightthickness=0,highlightcolor='black')
        self.grid(row=coord[0],column=coord[1])
        self.color=color
        self.coord=coord
        self.isKing=False
        if color == 'dark green' and coord[0] != 3 and coord[0] != 4:

            # create red checker
            if coord[0] < 4:
                self.create_oval(10,10,40,40,fill='red')
                self.checkerColor='red'
                self.hasChecker=True

            # create white checker
            else:
                self.create_oval(10,10,40,40,fill='white')
                self.checkerColor='white'
                self.hasChecker=True
        else:
            self.checkerColor=''
            self.hasChecker=False
        self.isSelected=False
        self.bind('<Button-1>',self.change_selection)

    def has_checker(self,color=''):
        '''CheckerSquare.has_checker(color)
        returns a boolean concering the checker or its color'''
        if color != '':
            return (self.checkerColor == color)
        else:
            return self.hasChecker

    def is_king(self):
        '''CheckerSquare.is_king(color)
        returns a boolean concering the checker's social status'''
        return self.isKing
    
    def crown(self):
        '''CheckerSquare.crown()
        crowns the checker'''
        self.isKing=True
        self['bg']='black'
    
    def change_selection(self,event):
        '''CheckerSquare.change_selection(event)
        event handler for mouse click
        changes square selection'''

        # update square
        if (self.isSelected == False) and (self.hasChecker == True):
            self.isSelected=True
            self['bg']='yellow'
            self.master.wait_for_move(self.coord,self.checkerColor)

        # reset square
        else:
            if self.hasChecker == True:
                self.master.change_group_bindings()
                self.master.change_group_bindings(self.checkerColor,'reset')
            self.isSelected=False
            if self.isKing == True:
                self['bg']='black'
            else:
                self['bg']=self.color

    def change_binding(self,change=''):
        '''CheckerSquare.change_binding(change)
        changes mouse assignments according to change'''
        self.unbind('<Button-1>')
        if change=='reset':
            self.bind('<Button-1>',self.change_selection)
        elif change=='wait for move':
            self.bind('<Button-1>',self.move_checker)

            
    def change_checker_state(self,color,king=False):
        '''ReversiSquare.make_color(color)
        changes color of piece on square to specified color'''

        # create new checker
        if self.hasChecker == False:
            self.create_oval(10,10,40,40,fill=color)
            self.hasChecker=True
            if king == True:
                self['bg']='black'
            else:
                self['bg']='dark green'
            self.isKing=king
            self.checkerColor=color

        # delete checker
        else:
            self.delete(self.find_all())
            if self.isKing == True:
                self['bg']='dark green'
            else:
                self['bg']=self.color
            self.isKing=False
            self.hasChecker=False
            self.isSelected=False
            self.checkerColor=''

    
    def move_checker(self,event):
        '''ReversiSquare.make_color(color)
        tells parent to move the checker'''
        self.master.move_checker(self.coord)
        

        
class CheckerGame(Frame):
    '''represents a game of Checkers'''
    
    def __init__(self,master):
        '''CheckerGame(master)
        creates a new Checkers game'''
        Frame.__init__(self,master)
        self.grid()
        self.squares={}
        
        # create board
        for row in range(8):
            for column in range(8):
                coord=(row,column)
                pColor='dark green'
                sColor='blanched almond'
                if column %2 == 0:
                    pColor='blanched almond'
                    sColor='dark green'
                if row%2 == 0:
                    self.squares[coord] = CheckerSquare(self,pColor,(row,column))
                else:
                    self.squares[coord] = CheckerSquare(self,sColor,(row,column))
                    
        # create labels
        self.turnSquare = CheckerSquare(self,'gray',(9,3))
        self.turnSquare.change_checker_state('red')
        self.turnSquare.change_binding()
        Label(self,text='Turn:',font=('Arial',12)).grid(row=9,column=2)
        self.gameLabel=Label(self,font=('Arial',12))
        self.gameLabel.grid(row=9,column=5,columnspan=12)
        self.change_group_bindings(color='white')
        
    def wait_for_move(self,coord,checkerColor):
        '''CheckerGame.wait_for_move(coord,checkerColor)
        prepares listeners for possible moves'''
        self.original=coord
        self.checkerColor=checkerColor
        if checkerColor=='red':
            self.oppositeColor='white'
        else:
            self.oppositeColor='red'
            
        # plant listeners
        self.change_group_bindings(color=checkerColor)
        self.squares[coord].change_binding('reset')

        # get available moves
        movesList=self.determine_moves(coord,moveType='special',color=checkerColor)
        self.prevMoves=movesList
        if len(movesList)==0:
            movesList=self.determine_moves(coord,moveType='normal',color=checkerColor)
        for m in movesList:
            self.squares[m].change_binding('wait for move')
                        
    
    def determine_moves(self,coord,color,moveType='normal'):
        '''CheckerGame.determine_moves(coord,color,moveType)
        calculates possible moves based for coord based on moveType'''
        mList=()
        if color=='red':
            mList=(-200,1)
            oppositeColor='white'
        else:
            mList=(-1,200)
            oppositeColor='red'
        if self.squares[coord].is_king():
            mList=(-1,1)
        moveList=[]

        # loop through forward and backward moves
        for m in mList:

            # special move
            if moveType != 'normal':            
                for c in (coord[1]-1,coord[1]+1):
                    d=c-coord[1]
                    if -1 < coord[0]+2*m < 8 and -1 < c+d < 8:
                        if self.squares[(coord[0]+2*m,c+d)].has_checker() == False and self.squares[(coord[0]+m,c)].has_checker(oppositeColor) == True:
                            moveList.append((coord[0]+2*m,c+d))

            # normal move
            else:   
                for c in (coord[1]-1,coord[1]+1):
                    if -1 < coord[0]+m < 8 and -1 < c < 8:
                        if self.squares[(coord[0]+m,c)].has_checker() == False:
                            moveList.append((coord[0]+m,c))
        return moveList
    
    def move_checker(self,coord):
        '''CheckerGame.move_checker(coord)
        moves coord around and checks for in-game events'''
        self.gameLabel['text']=''
        crown=False
        if self.squares[self.original].is_king():
            crown=True

        # move checkers and crowned checkers alike
        self.squares[self.original].change_checker_state(self.checkerColor,crown)
        self.squares[coord].change_checker_state(self.checkerColor,crown)
        
        # prepare for special move
        jumpInProgress=False
        for prev in self.prevMoves:
            if prev == coord:
                jumpInProgress = True
                break
        self.prevMoves=[]
        if jumpInProgress == True:
            self.squares[(((coord[0]-self.original[0])/2)+self.original[0],((coord[1]-self.original[1])/2)+self.original[1])].change_checker_state(self.oppositeColor)

        # prepare for multiple moves
        nextMoves=self.determine_moves(coord,moveType='special',color=self.checkerColor)
        if len(nextMoves) < 1:
            jumpInProgress=False
            
        # prepare next turn
        if (jumpInProgress==False):
            self.change_group_bindings(action='reset')
            for i in range(2):
                self.turnSquare.change_checker_state(self.oppositeColor)
            self.change_group_bindings(color=self.checkerColor)
            self.change_group_bindings(color=self.oppositeColor,action='reset')

        # prepare next move
        else:
            self.gameLabel['text']='Must Continue Jump'
            self.squares[coord].change_selection('')
            self.change_group_bindings()
            for move in nextMoves:
                self.squares[move].change_binding('wait for move')

        # check for in-game events
        self.check_for_kings()
        self.check_for_winner(self.checkerColor)
        
    def change_group_bindings(self,color='',action=''):
        '''CheckerGame.change_group_bindings(action,color)
        changes bindings to action for color group of squares'''

        # change certain squares
        if color != '':
            for square in self.squares:
                if self.squares[square].has_checker(color) == True:
                    self.squares[square].change_binding(action)

        # change all squares
        else:
            for square in self.squares:
                self.squares[square].change_binding(action)

    def check_for_kings(self):
        '''CheckerGame.check_for_kings()
        checks for checker crownings'''
        for row in (0,7):
            for column in range(8):

                # white checker crown
                if row==0:
                    if self.squares[(row,column)].has_checker('white'):
                        self.squares[(row,column)].crown()

                # red checker crown
                else:
                    if self.squares[(row,column)].has_checker('red'):
                        self.squares[(row,column)].crown()
                        
    def check_for_winner(self,color):
        '''CheckerGame.check_for_winner()
        checks for a winner'''
        if color=='red':
            ocolor='white'
        else:
            ocolor='red'
        movableList=[s for s in self.squares if (self.squares[s].has_checker(ocolor) == True) and (len(self.determine_moves(s,ocolor))+len(self.determine_moves(s,ocolor,'special')) > 0)]

        # found a winner
        if len(movableList) == 0:
            self.change_group_bindings()
            self.turnSquare.change_checker_state(color)
            self.gameLabel['text']=(str(color)).capitalize()+' wins!'
            
root = Tk()
root.title('Checkers')
Checkers = CheckerGame(root)
Checkers.mainloop()
