from images import images
import pygame
from utils.resizingFuncs import blitResized

class Tile:
    def __init__(self, pos, color, appearedTime = 0, disappearTime = 0, type = None):
        self.pos = pos
        self.color = color
        self.scale = 0
        self.appearedTime = appearedTime        
        self.disappearTime = disappearTime
        self.type = type
        self.factor = 1
        
        self.inputs = []
    
    def isOver(self, pos):
        return self.pos >= pos and self.pos <= pos + self.getTypeSize()
    
    def getTypeImage(self): #not using a dictionary because of copy by reference shenanigans
        match self.type:
            case "platform":
                return images.images["platform"]
            case "rest":
                return images.images["rest"]
            case "wall":
                return images.images["debug"] #for testing
    
    def getScaleFromAppearAnimTime(self, timeIntoAppearAnim, appearLength): #temp, to be replaced with proper animation
        return timeIntoAppearAnim / appearLength
    
    def toValues(self):
        return [self.pos, self.color, self.appearedTime, self.disappearTime, self.type]
    
    def getScaleFromDisappearAnimTime(self, timeIntoDisappearAnim, disappearLength): #temp, to be replaced with proper animation
        return 1 - (timeIntoDisappearAnim / disappearLength)    

    def draw(self, win, topLeftPos, tileSize, appearLength, disappearLength, time):
        if time < self.appearedTime - appearLength: #TODO: make tiles animate with a proper animatino
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
        
        pos = ((self.pos - topLeftPos) * tileSize + tileSize.multiply(1 - scale).divide(2))
        pos = pos.multiply(self.factor).toTuple()
        tileSize = tileSize.multiply(self.factor)
        #blitResized(win, self.getTypeImage(), pos, scale, self.factor)
        win.blit(pygame.transform.scale(self.getTypeImage(), tileSize.multiply(scale).toTuple()), pos)
        
    def copy(self):
        return Tile(self.pos, self.color, self.appearedTime, self.disappearTime, self.type)