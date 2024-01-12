# external imports
import pygame

# internal imports
from ui.button import Button
from utils.polygon import Polygon
from utils.vector2 import Vector2
from input import input

class InputBox(Button):
    def __init__(self, text, x, y, width, height, color, textColor, textSize = 40, sizeLocked = False, maxLength = 20, scaler = 1.25, clearOnInput = True, numOnly = False, hColor = None, textFont = "ROG"):
        Button.__init__(self, text, x, y, width, height, color, textColor, self.select, textSize=textSize, scaler=scaler, hColor=hColor, textFont=textFont)
        self.defaultText = text
        self.clearOnInput = clearOnInput
        self.active = False
        self.textColor = textColor
        self.highlightRect = Polygon.fromRect((self.x, self.y, self.width, self.height), self.textColor)
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.output = "" if self.clearOnInput else self.text.text
        self.returned = False
        self.numOnly = numOnly
        self.editable = True
        
    def accept(self):
        self.returned = False
        if self.clearOnInput:
            self.text.text = self.defaultText
            self.output = ""
        
    def deselect(self):
        if self.active:
            if self.clicked and self.text.text == "":
                self.clicked = False
                self.text.text = self.defaultText
            self.active = False
        
    def select(self):
        if not self.active and (not self.returned or not self.clearOnInput) and self.editable:
            if not self.clicked:
                self.text.text = ""
                self.clicked = True
            self.active = True
        
    def changeText(self, text):
        self.text.text = text
        self.defaultText = self.text.text
        self.output = self.text.text
        
    def update(self, pos = Vector2(0, 0)):
        Button.update(self, pos)
        if self.active:
            if not self.editable:
                self.deselect()
                return
            for key, value in input.characterBindings.items():
                if value.justPressed:
                    if not self.numOnly or (key.isdigit() or key == "."): self.text.text += key 
                    
            if input.specialKeyBindings["backspace"].justPressed:
                self.text.text = self.text.text[:-1]
                
            if input.specialKeyBindings["escape"].justPressed:
                self.active = False
                
            if input.specialKeyBindings["enter"].justPressed:
                self.output = self.text.text
                self.returned = True
                self.active = False
                
            if input.mouseBindings["lmb"].justPressed:
                if not self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.deselect()
        
    def draw(self, win, pos = Vector2(0, 0)):
        Button.draw(self, win, pos)
        if self.active:
            self.highlightRect.scale = self.scale
            self.highlightRect.draw(win, 2, pos = pos)