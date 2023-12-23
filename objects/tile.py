from images import images
import pygame
from utils.vector2 import Vector2
from objects.player import Player

class Tile:
    def __init__(self, pos, color, appearedTime = None, disappearTime = None, type = None):
        self.pos = pos
        self.color = color
        self.appearedTime = appearedTime
        self.disappearTime = disappearTime
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
    
    def getScaleFromAppearAnimTime(self, timeIntoAppearAnim, appearLength): #temp, to be replaced with proper animation
        return timeIntoAppearAnim / appearLength
    
    def getScaleFromDisappearAnimTime(self, timeIntoDisappearAnim, disappearLength): #temp, to be replaced with proper animation
        return 1 - (timeIntoDisappearAnim / disappearLength)    

    def draw(self, win, playerPos, appearLength, disappearLength, time):
        if time < self.appearedTime - appearLength: #this will be replaced with a proper animation once theres a good time to do that
            scale = 0
        elif time <= self.appearedTime:
            timeIntoAppearAnim = time - (self.appearedTime - appearLength)
            scale = self.getScaleFromAppearAnimTime(timeIntoAppearAnim, appearLength)
        elif time < self.disappearTime:
            scale = 1
        elif time <= self.disappearTime + disappearLength:
            timeIntoDisappearAnim = time - self.disappearTime
            scale = self.getScaleFromDisappearAnimTime(timeIntoDisappearAnim, disappearLength)
        else:
            scale = 0
        scale **= 5 #temp
        
        size = self.getTypeSize().multiply(scale).toTuple()
        pos = ((self.pos - playerPos + Player.offset) * self.getTypeSize() + self.getTypeSize().multiply(1 - scale).divide(2)).toTuple()
        win.blit(pygame.transform.scale(self.getTypeImage(), size), pos)