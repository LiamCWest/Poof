import pygame
from ui.button import Button
import input.input as input

class Scrollbar:
    def __init__(self, x, y, width, length, orientation, values, valueSize = None, bg = (0, 0, 0), fg = (255, 255, 255), z = 0):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.orientation = orientation
        self.W = self.width if self.orientation == "v" else self.length
        self.H = self.length if self.orientation == "v" else self.width
        self.bg = bg
        self.fg = fg
        self.values = values
        self.valueSize = valueSize if valueSize != None else self.length/len(self.values)
        self.z = z
        bW = self.width if self.orientation == "v" else self.valueSize
        bH = self.valueSize if self.orientation == "v" else self.width
        self.bar = Button("", self.x, self.y, bW, bH, self.fg, self.fg, lambda: None)
        
        self.value = 0
        self.perc = 0
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.W, self.H))
        self.bar.draw(screen)
    
    def move(self, perc):
        if self.orientation == "v":
            self.bar.y = self.y + perc*(self.length-self.valueSize)
        else:
            self.bar.x = self.x + perc*(self.length-self.valueSize)
        self.valUpdate()
    
    def update(self):
        self.bar.update()
        if self.bar.held:
            mPos = input.mousePos.y if self.orientation == "v" else input.mousePos.x
            newPos = mPos - self.valueSize//2
            pos = self.y if self.orientation == "v" else self.x
            if newPos > pos and newPos < pos+self.length-self.valueSize:
                if self.orientation == "v":
                    self.bar.y = newPos
                else:
                    self.bar.x = newPos
                self.valUpdate()

    def valUpdate(self):
        barPos = self.bar.y if self.orientation == "v" else self.bar.x
        pos = self.y if self.orientation == "v" else self.x
        self.perc = round((barPos-pos)/(self.length-self.valueSize), 1)
        self.value = round(self.perc * (len(self.values)-1))
