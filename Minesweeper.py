from tkinter import *
from tkinter import messagebox
import random

class MsCell(Label):
    '''creates a minesweeper cell'''

    def __init__(self,master,coord='',item=''):
        '''MsCell(master,item,coord) -> MsCell
        creates a new minesweeper tile with coord as its location
        and item the item it contains'''
        
        # set up descriptors
        Label.__init__(self,master,height=1,width=2,bg='light gray',font=('Arial',24),relief=RAISED)
        self.coord=coord
        self.item=item
        self['text']=''
        self.frozen=False
        self.colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']

        # set up buttons
        self.bind('<Button-1>',self.reveal)
        self.bind('<Button-3>',self.flag)
        
    def reveal(self,event):
        '''MsCell.reveal()
        reveals the item it contains'''
        
        self.focus_set()
        if self['text'] != '*' and self.frozen == False and self.master.get_game_state() == False:
            
            # update descriptors
            if str(self.item).isdigit():
                self['fg']=self.colormap[int(self.item)]
            self['relief']=SUNKEN

            # update image
            if self.item=='mine':
                self['text']='*'
                self['bg']='red'
            else:
                self['bg'] = 'light gray'
                self['text']=str(self.item)
            self.frozen=True

            # communicate to master
            if self.item == 'mine':
                self.master.reveal_cells(self.coord,True)
            if self.item == '':
                self.master.reveal_cells(self.coord)
            self.master.check_for_ending()
            
    def flag(self,event):
        '''MsCell.flag()
        flags the tile'''

        # change text
        
        if self.frozen == False and self.master.get_game_state() == False:
            if self['text'] == '*':
                self['text']=''
                self.master.change_flag_count(1)
            elif self.master.get_flag() != 0:
                self['text']='*'
                self.master.change_flag_count(-1)

    def get_item(self):
        '''MsCell.get_item()
        returns the item it represents'''
        
        return self.item

    def set_item(self,item):
        '''MsCell.set_item()
        changes the item it represents'''
        
        self.item=item

    def get_coord(self):
        '''MsCell.get_item()
        returns a tuple containing its location'''
        
        return self.coord

    def is_frozen(self):
        '''MsCell.is_frozen()
        returns a boolean that checks whether the tile is frozen'''
        
        return self.frozen

class MineUnit:
    '''creates a unit of minesweeper cells'''

    def __init__(self,cells):
        '''MineUnit(cells) -> MineUnit
        creates a group of minesweeper cells'''
        self.cells = cells  # store dict of SudokuCells
        
    def get_cell_list(self):
        '''MineUnit.get_cell_list()
        returns a list of (row,column) tuples of minesweeper cells'''
        return self.cells
                
    
class MineFrame(Frame):
    '''creates a frame of minesweeper cells'''

    def __init__(self,master,l,w,m):
        '''MineFrame(master)
        creates a new blank minesweeper frame'''
        
        # set up board
        Frame.__init__(self,master,bg='black')
        self.grid()
        self.cells = {}
        self.listOfCells=[]
        self.cellUnit={}
        self.flagNum=m
        
        # create a flag label
        self.scoreLabel = Label(self,text=str(self.flagNum),height=1,width=2,bg='white',font=('Arial',24))
        self.scoreLabel.grid(row=l*2+3,column=w-1,columnspan=2)
        
        # create frame
        for row in range(l):
            for column in range(w):
                cellList=[]
                coord = (row,column)
                self.listOfCells.append(coord)
                self.cells[coord] = MsCell(self,coord,'')
                self.cells[coord].grid(row=2*row,column=2*column)
                
                # create Units
                for r in range(coord[0]-1,coord[0]+2):
                    for c in range(coord[1]-1,coord[1]+2):
                        if -1 < r < l and -1 < c < w:
                            cellList.append((r,c))
                        self.cellUnit[coord]=MineUnit(cellList)
                        
        self.isDone=False
        self.winState=True

        # make mine cells
        mineList=[]
        for i in range(1,self.flagNum+1):
            choice=random.choice(self.listOfCells)
            mineList.append(choice)
            self.listOfCells.remove(choice)
        self.cellUnit['mine']=MineUnit(mineList)
        for element in mineList:
            self.cells[element].set_item('mine')

        # make cells communicate to each other
        for cell in self.listOfCells:
            numMines=0
            if self.cells[cell].get_item() != 'mine':
                for c in self.cellUnit[cell].get_cell_list():
                    if self.cells[c].get_item() == 'mine':
                        numMines+=1

                # determine other cells
                if numMines == 0:
                    self.cells[cell].set_item('')
                else:
                    self.cells[cell].set_item(numMines)
        
    def reveal_cells(self,cell,isMine=False):
        '''MineFrame.reveal_cells()
        reveals a set amount of cells'''
        
        if self.isDone == False:
            # reveal nearby mines
            if isMine == False:
                    for cells in self.cellUnit[cell].get_cell_list():
                        self.cells[cells].reveal('')
                        
            else:
                # reveal all mines
                for cells in self.cellUnit['mine'].get_cell_list():
                    self.cells[cells].reveal('')
                
                
    def change_flag_count(self,change):
        '''MineFrame.change_flag_count()
        changes the flag number displayed'''
        
        # change flag counter
        if self.flagNum != 0 or change == 1:
            self.flagNum+=change
        self.scoreLabel['text']=str(self.flagNum)
        
    def get_flag(self):
        '''MineFrame.get_flag()
        returns the flag number'''
        
        return self.flagNum
            
    def get_game_state(self):
        '''MineFrame.get_game_state()
        returns if the game is over'''
        return self.isDone
    
    def check_for_ending(self):
        '''MineFrame.check_for_ending()
        creates a game ending'''
        
        # create list of frozen and mine cells
        if self.isDone == False:
            normalCells=[c for c in self.cells if self.cells[c].get_item() != 'mine']
            mineCells=[c for c in self.cells if self.cells[c].get_item() == 'mine']
            self.reveal=0

            # check ending conditions
            for f in normalCells:
                if self.cells[f].is_frozen() == True:
                    self.reveal+=1

            # display ending message
            for mine in mineCells:
                if self.cells[mine].is_frozen() == True:
                    self.isDone=True
                    messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
                    break
            if self.reveal == len(normalCells):
                self.isDone=True
                messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

root = Tk()
root.title('MineSweeper')
l=int(input('Enter the board length here (default is 12): '))
w=int(input('Enter the board width here (default is 10): '))
m=int(input('Enter the number of mines here (default is 15): '))
minesweeper = MineFrame(root,l,w,m)
minesweeper.mainloop()
