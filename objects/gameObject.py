import pygame
from utils import drawDebug as dd

class GameObject:
    def __init__(self, pos, width, height, color, image = None):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        print(image)
        if image:
            self.image = pygame.image.load(dd.verifyTexture(image))
            self.imageRect = self.image.get_rect()
        else:
            self.image = None
        
    def draw(self, win):
        if self.image == None:
            pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, self.width, self.height))
        else:
            win.blit(self.image, (self.pos.x, self.pos.y))
            
    def update(self):
        pass
    
    def handleEvent(self, event):
        pass