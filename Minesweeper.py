import tkinter
import random
from tkinter import *


WIDTH = 800    
HEIGHT = 600
cell_size = 40

field_height = HEIGHT // cell_size
field_width = WIDTH // cell_size


class Game(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")
        
        self.c = Canvas(self.root, width = WIDTH, height = HEIGHT, bg = "black")
        self.c.pack()
        
        self.c.bind("<Button 1>", self.OpenCell)
        self.c.bind("<Button 3>", self.ThinkItsBomb)
        
        self.Predictions = {}

        self.MainCells = Grid(self, field_height, field_width)
        
        self.firstRandom = True

    
    def ThinkItsBomb(self, event):
        x = event.x // cell_size
        y = event.y // cell_size
        
        if self.MainCells.cells[y][x].opened == True:
            return None
        
        if self.MainCells.cells[y][x].prediction == False:
            self.MainCells.cells[y][x].prediction = True
            self.Predictions[str(x) + ' ' + str(y)] = (self.c.create_oval(x*cell_size,
                                                                          y*cell_size,
                                                                         (x + 1)*cell_size,
                                                                         (y + 1)*cell_size,
                                                                          fill = "red"))
        else:
            self.MainCells.cells[y][x].prediction = False
            self.c.delete(self.Predictions[str(x) + ' ' +  str(y)])
            self.Predictions.pop(str(x) + ' ' + str(y))
            

    

    def lose(self):
        self.c.delete("all")
        self.c.create_text(WIDTH // 2, HEIGHT // 2, 
                           text = "You lost", 
                           font = ("Purisa", 60), 
                           fill = "#32CD32")
        #self.root.destroy()


    
    def OpenNear(self, x, y):
        print("near x = {}; y = {}".format(x, y))
        for i in range(-1,2):
            for j in range(-1,2):
                if (not i == 0) or (not j == 0):
                    ix = (x + i)
                    iy = (y + j)
                    if ix >= 0 and ix < field_width and iy >= 0 and iy < field_height:
                        if self.MainCells.cells[iy][ix].opened == True:
                            continue
                        self.MainCells.cells[iy][ix].Open()
                        self.MainCells.cells[iy][ix].opened = True
                        if self.MainCells.cells[iy][ix].Nb == 0:
                            self.OpenNear(ix,iy)

    def OpenCell(self, event = None, x = 0, y = 0):
        if not event == None:
            x = event.x // cell_size
            y = event.y // cell_size

        if self.MainCells.cells[y][x].opened == True or self.MainCells.cells[y][x].prediction == True:
            return None

        self.MainCells.cells[y][x].opened = True
        print("click x = {}; y = {}".format(x, y))
        
        if (self.firstRandom == True):
            while True:
                self.MainCells.RandomIt()
                self.MainCells.UpdateCells()
                self.firstRandom = False
                if(self.MainCells.cells[y][x].bomb == False):
                    break
        
        if(self.MainCells.cells[y][x].Nb == 0):
            self.OpenNear(x, y)
        self.MainCells.cells[y][x].Open()

class Segment(object):
    def __init__(self,game, x, y, bomb):
        self.instance = game.c.create_rectangle(x*cell_size, y*cell_size, 
                                               (x + 1)*cell_size, (y + 1)*cell_size,
                                                fill = "white")
        self.x = x
        self.y = y
        self.game = game
        self.bomb = bomb
        self.opened = False
        self.prediction = False

    def Open(self):
        if(self.bomb == True):
            self.game.c.itemconfigure(self.instance, fill = "green")
            self.game.lose()
        else: 
            self.game.c.create_text(self.x*cell_size + cell_size / 2, 
                                    self.y*cell_size + cell_size / 2, 
                                    font=("Purisa", cell_size // 2),
                                    text = "{}".format(self.Nb))

    def CountNeightbors(self, WholeGrid):
        if (self.bomb == True):
            return None
        self.Nb = 0
        if not self.bomb == True:
            for x in range(-1,2):
                for y in range(-1,2):
                    if (not x == 0) or (not y == 0):
                        ix = (self.x + x)
                        iy = (self.y + y)
                        if ix >= 0 and ix < field_width and iy >= 0 and iy < field_height:
                            if WholeGrid.cells[iy][ix].bomb == True:
                                self.Nb = self.Nb + 1

class Grid(object):

    def __init__(self, game, H, W):
        self.cells = []
        for line in range(H):
            a = []
            for cell in range(W):
                a.append(Segment(game, cell, line, False))
            self.cells.append(a)

    def RandomIt(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                self.cells[line][cell].bomb = random.choice([True, False, False, False, False, False, False, False])
                if self.cells[line][cell].bomb == True:
                    self.cells[line][cell].Nb = -1
    
    def UpdateCells(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                self.cells[line][cell].CountNeightbors(self)








game = Game()

game.root.mainloop()