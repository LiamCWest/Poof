import pygame
from ui.button import Button
import input.input as input

class Scrollbar:
    def __init__(self, x, y, width, length, orientation, values, valueSize = None, bg = (0, 0, 0), fg = (255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.orientation = orientation
        self.bg = bg
        self.fg = fg
        self.values = values
        self.valueSize = valueSize if valueSize != None else self.length/len(self.values)
        self.bar = Button("", self.x, self.y, self.width, self.valueSize, self.fg, self.fg, lambda: None)
        
        self.value = 0
        self.perc = 0
        
    def draw(self, screen): #TODO: orientation fix
        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.width, self.length))
        self.bar.draw()
    
    def update(self):
        self.bar.update()
        if self.bar.held:
            newY = input.mousePos.y - self.valueSize//2
            if newY > self.y and newY < self.y+self.length-self.valueSize:
                self.bar.y = newY
                self.valUpdate()

    def valUpdate(self):
        self.perc = round((self.bar.y-self.y)/(self.length-self.valueSize), 1)
        self.value = round(self.perc * (len(self.values)-1))