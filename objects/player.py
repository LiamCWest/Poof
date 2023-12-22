from images import images
import pygame
from utils.vector2 import Vector2

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.realPos = pos
        
    def draw(self, win):
        size = Vector2(50, 50)
        img = images.images["player"]
        
        win.blit(pygame.transform.scale(img, size.toTuple()), (size * Vector2(5, 4)).toTuple())