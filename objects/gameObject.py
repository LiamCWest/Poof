import pygame
from utils import drawDebug as dd
from utils.vector2 import Vector2

class GameObject:
    def __init__(self, pos, width, height, color, image = None):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.imageScale = Vector2(1,1)
        if image:
            self.image = pygame.image.load(dd.verifyTexture(image))
            self.imageRect = self.image.get_rect()
            self.imageScale = Vector2(self.width / self.imageRect.width, self.height / self.imageRect.height)
        else:
            self.image = None
        
    def draw(self, win):
        if self.image == None:
            pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, self.width, self.height))
        else:
            win.blit(pygame.transform.scale_by(self.image, (self.imageScale.x, self.imageScale.y)), (self.pos.x, self.pos.y))
            
    def update(self):
        pass