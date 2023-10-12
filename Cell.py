import pygame
from Colors import *

class Cell:
    def __init__(self, window, x=0, y=0, width=20, height=20, color=WHITE):

        #dimensions
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.edgeWidth = 1

        #colors
        self.mainColor = color
        self.altColor = BLACK
        self.currColor = color

        #pygame
        self.window = window
        self.recentlyClicked = False

    def draw(self):
        pygame.draw.rect(self.window, self.currColor, (self.x+1, self.y+1, self.width-2, self.height-2))

    def clicked(self, held=False):
        
        if(self.currColor == self.mainColor) and not self.recentlyClicked:
            self.currColor = self.altColor
        elif not self.recentlyClicked and not held:
            self.currColor = self.mainColor

        self.recentlyClicked = True

    def refresh(self):
        self.recentlyClicked = False

class Node(Cell):
    def __init__(self, window, x=0, y=0, width=20, height=20, color=WHITE):
        super().__init__(window, x, y, width, height, color)
        
        #dimensions 
        self.radius = width

    def draw(self):
        pygame.draw.circle(self.window, self.currColor, (self.x, self.y), self.radius, self.edgeWidth)