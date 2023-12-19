import pygame

class GameObject:
    def __init__(self, x, y, width, height, color, image = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        
    def draw(self, win):
        if self.image == None:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        else:
            win.blit(self.image, (self.x, self.y))
            
    def update(self):
        pass
    
    def handleEvent(self, event):
        pass