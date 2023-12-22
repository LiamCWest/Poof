from images import images
import pygame
from utils.vector2 import Vector2

class Tile:
    def __init__(self, pos, color, appearedTime = None, disappearedTime = None, type = None):
        self.pos = pos
        self.color = color
        self.appearedTime = appearedTime
        self.disappearedTime = disappearedTime
        self.type = type
    
    def getTypeImage(self): #not using a dictionary because of copy by reference shenanigans
        match self.type:
            case "platform":
                return images.images["platform"]
            case "rest":
                return images.images["rest"]
            case "wall":
                return images.images["debug"] #for testing
    
    def getTypeSize(self):
        return Vector2(50, 50)

    def draw(self, win, playerPos):
        win.blit(pygame.transform.scale(self.getTypeImage(), self.getTypeSize().toTuple()), ((self.pos - playerPos) * self.getTypeSize()).toTuple())