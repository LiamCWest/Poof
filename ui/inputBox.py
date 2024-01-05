from ui.button import Button
from ui.text import Text
from utils.polygon import Polygon
from graphics import gui
from input import input
import pygame

class InputBox(Button):
    def __init__(self, text, x, y, width, height, color, textColor, textSize = 40, sizeLocked = False, maxLength = 20):
        Button.__init__(self, text, x, y, width, height, color, textColor, self.select)
        self.defaultText = text
        self.active = False
        self.textColor = textColor
        self.highlightRect = Polygon.fromRect((self.x, self.y, self.width, self.height), self.textColor)
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def deselect(self):
        if self.active: 
            if self.clicked and self.text.text == "":
                self.clicked = False
                self.text.text = self.defaultText
            self.active = False
        
    def select(self):
        if not self.active:
            if not self.clicked:
                self.text.text = ""
                self.clicked = True
            self.active = True
        
    def update(self):
        Button.update(self)
        if self.active:
            for key, value in input.characterBindings.items():
                if value.justPressed:
                    self.text.text += key
                    
            if input.specialKeyBindings["backspace"].justPressed:
                self.text.text = self.text.text[:-1]
                
            if input.specialKeyBindings["escape"].justPressed or input.specialKeyBindings["enter"].justPressed:
                self.active = False
                
            if input.mouseBindings["lmb"].justPressed:
                if not self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.deselect()
        
    def draw(self, win):
        Button.draw(self, win)
        if self.active:
            self.highlightRect.scale = self.scale
            self.highlightRect.draw(win, 2)