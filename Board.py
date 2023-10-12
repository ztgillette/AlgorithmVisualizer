import random
import time
from Cell import *
from Algorithms import *


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
        self.clockcounter = 0
        self.clockmax = 60

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
        self.algorithm = Algorithms()
        self.algo = "BFS"
        self.currentCell = None
        self.visitedCells = []
        self.celllist = []
        self.neighbors = []
        self.parentCells = {}
        self.path = []
        self.backtrack = None
        self.running = False
        self.live = False
        self.started = False
        self.allowDiagonals = False
        self.paused = True

    def draw(self):
        self.window.fill(self.edgeColor)
        if self.live:
            self.drawAlgorithm()
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].draw()
        if self.live:
            self.undrawAlgorithm()
        
        

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

            #remove cell from celllist so it wont stomp on new square
            #will become a wall, so we don't want it to be a possible choice
            if(mycell.wall == False and mycell != self.goal and mycell!=self.start):
                if mycell in self.celllist:
                    self.celllist.remove(mycell)

    def detectMouseUnclick(self):
        self.mousePressed = False
        self.refreshCells()

    def refreshCells(self):
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].refresh()

    def resetCells(self):
        self.resetAlgorithm(self.algorithm)
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].reset()

    def fillRandom(self):
        self.resetCells()
        self.resetAlgorithm()
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                random_float = random.random()
                if(random_float > self.howRandom):
                    self.cell[i][j].makeWall()
                else:
                    self.cell[i][j].makeEmpty()
    
    def checkValidCell(self, cell, deltax, deltay):
        cellx = cell.xcoor
        celly = cell.ycoor

        if cellx + deltax >= 0 and cellx + deltax < self.numHorizontalCells and celly + deltay >= 0 and celly + deltay < self.numVerticalCells and self.cell[cellx+deltax][celly+deltay].wall == False:
            return True
        return False

    
    def getNeighbors(self, cell):

        neighbors = []
        x = cell.xcoor
        y = cell.ycoor

        #top left
        if self.checkValidCell(cell, -1, -1) and self.allowDiagonals:
            neighbors.append(self.cell[x-1][y-1])
        #top middle
        if self.checkValidCell(cell, 0, -1):
            neighbors.append(self.cell[x][y-1])
        #top right
        if self.checkValidCell(cell, 1, -1) and self.allowDiagonals:
            neighbors.append(self.cell[x+1][y-1])
        #middle left
        if self.checkValidCell(cell, -1, 0):
            neighbors.append(self.cell[x-1][y])
        #middle right
        if self.checkValidCell(cell, 1, 0):
            neighbors.append(self.cell[x+1][y])
        #bottom left
        if self.checkValidCell(cell, -1, 1) and self.allowDiagonals:
            neighbors.append(self.cell[x-1][y+1])
        #bottom center
        if self.checkValidCell(cell, 0, 1):
            neighbors.append(self.cell[x][y+1])
        #bottom right
        if self.checkValidCell(cell, 1, 1) and self.allowDiagonals:
            neighbors.append(self.cell[x+1][y+1])

        print("num neighbors: " + str(len(neighbors)))

        return neighbors
        
    def resetAlgorithm(self, algorithm=Algorithms()):
        self.algorithm = Algorithms()
        self.currentCell = None
        self.visitedCells = []
        self.celllist = []
        self.parentCells = {}
        self.neighbors = []
        self.path = []
        self.backtrack = None
        self.running = False
        self.live = False
        self.started

    def changeAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def drawAlgorithm(self):
        
        if self.currentCell != self.start and self.currentCell != self.goal and self.currentCell != None:
            self.currentCell.setColor(YELLOW)
        for n in self.neighbors:
            if n!= self.start and n!=self.goal and n!=None:
                n.setColor(PURPLE)
        
        #draw path
        for p in self.path:
            if p!= self.start and p!=self.goal and p!=None:
                p.setColor(GREEN)

    def undrawAlgorithm(self):

        #reset colors
        if self.currentCell != self.start and self.currentCell != self.goal and self.currentCell != None:
            self.currentCell.resetColor()
    
        for n in self.neighbors:
            if n!= self.start and n!=self.goal and n!=None:
                n.resetColor()
        
    def playpause(self):

        if(self.paused):
            self.paused = False
            self.running = True
            self.live = True
            self.started = True
        else:
            self.paused = True
            self.running = False
            self.started = False
    
    def setBFS(self):
        self.algo = "BFS"

    def setDFS(self):
        self.algo = "DFS"

    def setASTAR(self):
        self.algo = "A*"

    def speedup(self):
        if(self.clockmax > 5):
            self.clockmax -= 5
        else:
            self.clockmax = 1

    def slowdown(self):
        if(self.clockmax == 1):
            self.clockmax = 5
        elif(self.clockmax < 175):
            self.clockmax += 5

    

class Graph(Board):
   def init(self):
      pass