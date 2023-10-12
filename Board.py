import random
from Cell import *


class Board:
    def __init__(self, window, width, height, numXCells, numYCells, cellColor = GRAY, edgeColor = DARK_GRAY):

        #dimensions
        self.pixelWidth = width
        self.pixelHeight = height
        self.numHorizontalCells = numXCells
        self.numVerticalCells = numYCells
        self.cellWidth = width / numXCells
        self.cellHeight = height / numYCells

        #pygame
        self.window = window
        self.cellColor = cellColor
        self.edgeColor = edgeColor
        self.mouseX = 0
        self.moseY = 0

        #cell list
        self.cell = []
        for i in range(self.numHorizontalCells):
            #fill each row
            row = []
            for j in range(self.numVerticalCells):
                row.append(Cell(self.window, i*self.cellWidth, j*self.cellHeight, 
                                self.cellWidth, self.cellHeight, self.cellColor))
            self.cell.append(row)

        #board editing
        self.mousePressed = False
        self.howRandom = 0.7
                
        #algorithm variables
        self.start = self.cell[0][0]
        self.goal = self.cell[numXCells-1][numYCells-1]
        self.start.makeStart()
        self.goal.makeGoal()

    def draw(self):
        self.window.fill(self.edgeColor)
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].draw()

    def detectMouseHover(self):
        x, y = pygame.mouse.get_pos()
    
        # Display mouse coordinates in window title

        self.mouseX = x
        self.mouseY = y

        if(self.mousePressed):
            mycell = self.findCellAtPixelCoors(x,y)
            if mycell != None:
                mycell.clicked(held=True)

    def findCellAtPixelCoors(self, x, y):
        gridx = int(x // self.cellWidth)
        gridy = int(y // self.cellHeight)

        if(gridx >= 0 and gridx < self.numHorizontalCells and gridy >= 0 and gridy < self.numVerticalCells):
            return self.cell[gridx][gridy]
        
        return None

    def detectMouseClick(self, x, y):
        self.mousePressed = True
        mycell = self.findCellAtPixelCoors(x,y)
        if mycell != None:
            mycell.clicked()

    def detectMouseUnclick(self):
        self.mousePressed = False
        self.refreshCells()

    def refreshCells(self):
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].refresh()

    def resetCells(self):
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].reset()

    def fillRandom(self):
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                random_float = random.random()
                if(random_float > self.howRandom):
                    self.cell[i][j].makeWall()
                else:
                    self.cell[i][j].makeEmpty()

    
    

class Graph(Board):
   def init(self):
      pass