import pygame
from Colors import *
import math

class Cell:
    def __init__(self, window, x=0, y=0, width=20, height=20, color=WHITE):

        #dimensions
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xcoor = int(self.x/self.width)
        self.ycoor = int(self.y/self.height)
        self.edgeWidth = 1

        #colors
        self.mainColor = color
        self.altColor = BLACK
        self.currColor = color

        #pygame
        self.window = window
        self.recentlyClicked = False

        #algorithm
        self.wall = False
        self.start = False
        self.goal = False
        self.hcost = 0
        self.gcost = 0
        self.fcost = 0

    def draw(self):
        pygame.draw.rect(self.window, self.currColor, (self.x+1, self.y+1, self.width-2, self.height-2))

    def clicked(self, held=False):

        if not self.start and not self.goal:
            
            if(self.currColor == self.mainColor) and not self.recentlyClicked:
                self.makeWall()
            elif not self.recentlyClicked and not held:
                self.makeEmpty()

            self.recentlyClicked = True

    def refresh(self):
        self.recentlyClicked = False

    def reset(self):
        if not self.start and not self.goal:
            self.currColor = self.mainColor
            self.recentlyClicked = False
            self.wall = False
            self.hcost = 0
            self.gcost = 0
            self.fcost = 0

    def makeWall(self):
        if not self.start and not self.goal:
            self.wall = True
            self.currColor = self.altColor

    def makeEmpty(self):
        if not self.start and not self.goal:
            self.wall = False
            self.currColor = self.mainColor

    def makeStart(self):
        self.start = True
        self.currColor = GREEN
    
    def makeGoal(self):
        self.goal = True
        self.currColor = RED

    def setColor(self, color):
        self.currColor = color

    def resetColor(self):
        self.currColor = self.mainColor

    def calculateGCost(self, parent):

        #calculate distance from parent
        deltax = abs(parent.xcoor - self.xcoor)
        deltay = abs(parent.ycoor - self.ycoor)

        self.gcost = parent.gcost + (deltax + deltay)

    def calculateHCost(self, goal):
        #heuristic is simply diagonal path length
        #a^2 + b^2 = c^2
        deltax = abs(self.xcoor-goal.xcoor)
        deltay = abs(self.ycoor-goal.ycoor)

        self.hcost = math.sqrt(deltax*deltax + deltay*deltay)

    def calculateFCost(self):
        self.fcost = self.hcost + self.gcost


class Node(Cell):
    def __init__(self, window, x=0, y=0, neighbors=[], width=20, height=20, color=WHITE):
        super().__init__(window, x, y, width, height, color)
        
        #dimensions 
        self.radius = width
        self.neighbors = neighbors
        self.edgeWidth = 2

        #edges
        self.drawnedges = []

    def draw(self):
        pygame.draw.circle(self.window, self.currColor, (self.x, self.y), self.radius, self.edgeWidth)
        

    def drawEdges(self, neighbors=-1, linecolor=BLACK, linewidth = 3):

        if(neighbors==-1):
            neighbors=self.neighbors

        for neighbor in neighbors:
            #calculate big hipotenuse 
            deltax = abs(self.x-neighbor.x)
            deltay = abs(self.y-neighbor.y)
            hyp = math.sqrt((deltax*deltax) + (deltay*deltay))

            minideltax = deltax * self.radius / (hyp+0.1)
            minideltay = deltay * self.radius / (hyp+0.1)

            #self is to the right of neighbor
            if(self.x > neighbor.x):
                newx = self.x - minideltax
                newx2 = neighbor.x + minideltax

                #self is below neighbor
                if(self.y > neighbor.y):
                    newy = self.y - minideltay
                    newy2 = neighbor.y + minideltay
                else:
                    newy = self.y + minideltay
                    newy2 = neighbor.y - minideltay


            #self is to the left of neighbor
            else:
                newx = self.x + minideltax
                newx2 = neighbor.x - minideltax

                #self is below neighbor
                if(self.y > neighbor.y):
                    newy = self.y - minideltay
                    newy2 = neighbor.y + minideltay
                else:
                    newy = self.y + minideltay
                    newy2 = neighbor.y - minideltay

            if neighbor not in self.drawnedges:
                pygame.draw.line(self.window, linecolor, (newx, newy), (newx2, newy2), linewidth)
                self.drawnedges.append(neighbor)
                neighbor.drawnedges.append(self)

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor) 
        neighbor.neighbors.append(self)

    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)
        neighbor.neighbors.remove(self)

    def getNumNeighbors(self):
        return len(self.neighbors)
    
    def isNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            return True
        return False