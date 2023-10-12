import pygame
import sys
from Colors import *

class Button:
    def __init__(self, window, function, x, y, width=150, height=50, buttontext = "Button", obj = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GRAY
        self.window = window
        self.fontsize = int(width / 6)
        self.font = pygame.font.SysFont('Arial', self.fontsize)
        self.buttontext = buttontext
        self.text = self.font.render(self.buttontext, True, BLACK)
        self.function = function
        self.obj = obj

    def draw(self):

        #button currently selected
        if(self.obj != None and self.obj.algo == self.buttontext):
            self.color = YELLOW
        else:
            self.color = GRAY

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height))
        self.window.blit(self.text, (self.x + (self.width//2) - (self.text.get_width()//2), self.y + (self.height//2) - (self.text.get_height()//2)))

    def press(self):
        self.function()

    def detectMouseClick(self, x, y):
        if(x >= self.x and x<= self.x+self.width and y >= self.y and y <= self.y+self.height):
            self.press()
