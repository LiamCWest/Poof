import pygame

class GameObject:
    def __init__(self, pos, width, height, color, image = None):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        
    def draw(self, win):
        if self.image == None:
            pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, self.width+self.pos.x, self.height+self.pos.y))
        else:
            win.blit(self.image, (self.x, self.y))
            
    def update(self):
        pass
    
    def handleEvent(self, event):
        pass