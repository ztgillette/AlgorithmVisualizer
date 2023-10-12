import pygame
from Colors import *

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

    def draw(self):
        pygame.draw.rect(self.window, self.currColor, (self.x+1, self.y+1, self.width-2, self.height-2))

    def clicked(self, held=False):

        if not self.start and not self.goal:
            
            if(self.currColor == self.mainColor) and not self.recentlyClicked:
                self.currColor = self.altColor
                self.wall = True
            elif not self.recentlyClicked and not held:
                self.currColor = self.mainColor
                self.wall = False

            self.recentlyClicked = True

    def refresh(self):
        self.recentlyClicked = False

    def reset(self):
        if not self.start and not self.goal:
            self.currColor = self.mainColor
            self.recentlyClicked = False
            self.wall = False

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

class Node(Cell):
    def __init__(self, window, x=0, y=0, width=20, height=20, color=WHITE):
        super().__init__(window, x, y, width, height, color)
        
        #dimensions 
        self.radius = width

    def draw(self):
        pygame.draw.circle(self.window, self.currColor, (self.x, self.y), self.radius, self.edgeWidth)