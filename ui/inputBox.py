from ui.button import Button
from ui.text import Text
from graphics import gui
from input import input
import pygame

class InputBox(Button):
    def __init__(self, text, x, y, width, height, color, textColor, textSize = 40):
        Button.__init__(self, text, x, y, width, height, color, textColor, self.select)
        self.active = False
        self.input = ""
        self.textColor = textColor
        self.text = Text(self.input, x + width//2, y + height//2, textColor, textSize)
        
    def select(self):
        print("select")
        if self.active: self.active = False
        else: self.active = True
        
    def update(self):
        Button.update(self)
        if self.active:
            pass
        
    def draw(self, win):
        Button.draw(self, win)
        if self.active:
            pygame.draw.rect(win, self.textColor, (self.x, self.y, self.width, self.height), 2)