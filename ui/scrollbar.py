import pygame

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
        
        self.value = 0
        
    def draw(self, screen): #TODO: orientation fix
        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.width, self.totalHeight))
        pygame.draw.rect(screen, self.fg, (self.x, self.y, self.width, self.height))
    
    def update(self):
        pass