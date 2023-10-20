import random
import time
from Cell import *
from Algorithms import *
from Button import *


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
        self.modeswitch = False
        self.mode = "Grid"
        self.buttons = []
        self.makeButtons()

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

    def makeButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.window, self.resetCells, 825, 25, 150, 50, "Reset"))
        self.buttons.append(Button(self.window, self.fillRandom, 825, 100, 150, 50, "Randomize"))
        self.buttons.append(Button(self.window, self.switchMode, 825, 175, 70, 50, "Grid", self))
        self.buttons.append(Button(self.window, self.switchMode, 905, 175, 70, 50, "Graph", self))

        self.buttons.append(Button(self.window, self.playpause, 825, 275, 150, 50, "Play / Pause"))
        self.buttons.append(Button(self.window, self.slowdown, 825, 350, 70, 50, "--Speed"))
        self.buttons.append(Button(self.window, self.speedup, 905, 350, 70, 50, "++Speed"))
        
        self.buttons.append(Button(self.window, self.setBFS, 825, 450, 150, 50, "BFS", self))
        self.buttons.append(Button(self.window, self.setDFS, 825, 525, 150, 50, "DFS", self))
        self.buttons.append(Button(self.window, self.setASTAR, 825, 600, 150, 50, "A*", self))
        
        

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
        if(len(self.cell) > 0):
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
                p.setColor(ORANGE)

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

    #used for A* (makes self.celllist into a priority queue)
    def addByPriority(self, cell):
        for i in range(len(self.celllist)):
            #compare with current cell
            if cell.fcost <= self.celllist[i].fcost:
                self.celllist.insert(i, cell)
                return
        self.celllist.append(cell)

    def switchMode(self):
        self.modeswitch = True
    

class Graph(Board):
    def __init__(self, window, width, height, numXCells, numYCells, cellColor = BLACK, edgeColor = DARK_GRAY):
        super().__init__(window, width, height, numXCells, numYCells, cellColor, edgeColor)

        self.cellColor = BLACK
        self.cell = []
        self.fillRandom()
        self.mode = "Graph"
        self.modeswitch = False

    def draw(self):
        self.window.fill(self.edgeColor)
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].drawEdges()

        if self.live:
            self.drawAlgorithm()
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                self.cell[i][j].draw()
                
        if self.live:
            self.undrawAlgorithm()

    def fillRandom(self):

        #clear current
        self.resetCells()
        self.path = []
        self.cell = []

        #start with some reasonable number of nodes
        numNodes = random.randint(25,50)

        #we want nodes to be distributed evenly, so lets divide graph board into numNodes sections
        hor = int(math.sqrt(numNodes * self.pixelWidth / self.pixelHeight))
        ver = int(numNodes/hor)
        numNodes = int(hor*ver)
        horpixelbox = int(self.pixelWidth/hor)
        verpixelbox = int(self.pixelHeight/ver)
        self.numHorizontalCells = hor
        self.numVerticalCells = ver

        #create nodes within compartments
        for i in range(hor):

            row=[]
        
            for j in range(ver):

                #x window is i*horpixelbox - (i+1)horpixelbox-1
                newcellx = random.randint(i*horpixelbox + self.cellWidth//2, (i+1)*horpixelbox-1 - self.cellWidth//2) 
                newcelly = random.randint(j*verpixelbox + self.cellWidth//2, (j+1)*verpixelbox-1 - self.cellWidth//2)

                newnode = Node(self.window, newcellx, newcelly, [],
                                    self.cellWidth, self.cellHeight, self.cellColor)
                
                row.append(newnode)
            
            self.cell.append(row)

        #create edges
        for i in range(hor):
            for j in range(ver):

                #recalculate x and y
                x = self.cell[i][j].x // horpixelbox
                y = self.cell[i][j].y // verpixelbox

                #only assign neighbors if even, even (all else will get by association)
                if x%2==0 and y%2==0:

                    for a in range(x-1, x+2):
                        for b in range(y-1, y+2):

                            if(a >= 0 and a < hor and b >= 0 and b < ver and (a != x or b != y)):

                                #random num
                                odds = random.randint(0,1)

                                if(odds == 0):
                                    self.cell[i][j].addNeighbor(self.cell[a][b])
        
        #connect disconnected nodes
        for i in range(hor):
            for j in range(ver):
                if self.cell[i][j].getNumNeighbors() == 0:
                    
                    #make a list of all possible neighbors
                    possibleNeighbors = []

                    #recalculate x and y
                    x = self.cell[i][j].x // horpixelbox
                    y = self.cell[i][j].y // verpixelbox

                    for a in range(x-1, x+2):
                        for b in range(y-1, y+2):
                            if(a >= 0 and a < hor and b >= 0 and b < ver and (a != x or b != y)):
                                possibleNeighbors.append((a, b))

                    #pick one of the possible neighbors at random
                    nx, ny = possibleNeighbors[random.randint(0, len(possibleNeighbors)-1)]
                    self.cell[i][j].addNeighbor(self.cell[nx][ny])

        self.start = self.cell[0][0]
        self.goal = self.cell[hor-1][ver-1]
        self.start.makeStart()
        self.goal.makeGoal()

        #make sure graph is connected
        self.makeConnected()

    def getNeighbors(self, cell):
        return cell.neighbors
    
    def drawAlgorithm(self):
        
        if self.currentCell != self.start and self.currentCell != self.goal and self.currentCell != None:
            self.currentCell.setColor(YELLOW)
        for n in self.neighbors:
            if n!= self.start and n!=self.goal and n!=None:
                n.setColor(PURPLE)
        
        #draw path
        for p in self.path:
            if p!= self.start and p!=self.goal and p!=None:
                p.setColor(ORANGE)

        #draw edges in path
        for i in range(len(self.path)-1):
            self.path[i].drawEdges([self.path[i+1]], ORANGE)

    def undrawAlgorithm(self):

        #reset colors
        if self.currentCell != self.start and self.currentCell != self.goal and self.currentCell != None:
            self.currentCell.resetColor()
    
        for n in self.neighbors:
            if n!= self.start and n!=self.goal and n!=None:
                n.resetColor()


    #sometimes fillRandom() makes 
    def makeConnected(self):
    
        visited = []
        for i in range(self.numHorizontalCells):
            row = []
            for j in range(self.numVerticalCells):
                row.append(0)
            visited.append(row)

        #while there are unvisited cells, we can't ensure that we are connected
        while(self.getUnvisited(visited) != None):

            #apply DFS and keep track of if we reach a node
            start = self.getUnvisited(visited)
            stack = [start]
            x = start.x // int(self.pixelWidth/self.numHorizontalCells)
            y = start.y // int(self.pixelHeight/self.numVerticalCells)
            visited[x][y] = 1

            lastvisited = start

            while(len(stack) > 0):

                node = stack.pop()
                lastvisited = node

                #get neighbors
                neighbors = node.neighbors

                for neighbor in neighbors:
                    x = neighbor.x // int(self.pixelWidth/self.numHorizontalCells)
                    y = neighbor.y // int(self.pixelHeight/self.numVerticalCells)
                    if visited[x][y] == 0:
                        stack.append(neighbor)
                        visited[x][y] = 1

            #if stack empty, see if all nodes have been visited. if not, we need to connect last node with next node
            if(self.getUnvisited(visited) != None):
                #connect lastvisited with next unvisited node (a.k.a getUnvisited())

                connected = False

                for neighbor in lastvisited.neighbors:
                    x = neighbor.x // int(self.pixelWidth/self.numHorizontalCells)
                    y = neighbor.y // int(self.pixelHeight/self.numVerticalCells)

                    if visited[x][y] == 0 and not connected:
                        lastvisited.addNeighbor(self.cell[x][y])
                        connected = True
                
                if not connected:
                    lastvisited.addNeighbor(self.getUnvisited(visited))
                    
    def getUnvisited(self, visited):
        for i in range(self.numHorizontalCells):
            for j in range(self.numVerticalCells):
                if visited[i][j] == 0:
                    return (self.cell[i][j])
        return None
    
    def switchMode(self):
        self.modeswitch = True

