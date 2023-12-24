import pygame
from ui.button import Button

class Scrollbar:
    def __init__(self, x, y, width, height, totalHeight, orientation, bg = (0, 0, 0), fg = (255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.totalHeight = totalHeight
        self.orientation = orientation
        self.bg = bg
        self.fg = fg
        self.bar = Button("", self.x, self.y, self.width, self.height, self.fg, self.fg, self.dragStart) #fix
        
        self.value = 0
        
    def draw(self, screen): #TODO: orientation fix
        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.width, self.totalHeight))
    
    def dragStart(self):
        while self.bar.held:
            self.bar.x = pygame.mouse.get_pos()[0]
    
    def update(self):
        pass