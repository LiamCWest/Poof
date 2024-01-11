from images import images
import pygame
import graphics.gui

class Tile:
    def __init__(self, pos, color, appearedTime = 0, disappearTime = 0, type = "platform", divisor = None):
        self.pos = pos
        self.color = color
        self.scale = 0
        self.appearedTime = appearedTime        
        self.disappearTime = disappearTime
        self.type = type
        self.divisor = divisor
    
    def isOver(self, pos):
        return self.pos >= pos and self.pos <= pos + self.getTypeSize()
    
    def getTypeImage(self): #not using a dictionary because of copy by reference shenanigans
        if self.type == "platform":
            return images.images["platform"]
        elif self.type == "glide":
            return images.images["glide"]
        else:
            return images.images["rest"]
    
    def getScaleFromAppearAnimTime(self, timeIntoAppearAnim, appearLength): #temp, to be replaced with proper animation
        return timeIntoAppearAnim / appearLength
    
    def toValues(self):
        return [self.pos, self.color, self.appearedTime, self.disappearTime, self.type, self.divisor]
    
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
        
        pos = ((self.pos - topLeftPos) * tileSize + tileSize.multiply(1 - scale).divide(2)).toTuple()
        win.blit(pygame.transform.scale(self.getTypeImage(), tileSize.multiply(scale).toTuple()), pos)
        
        if self.type == "glide":
            textPos = (self.pos.add(0.5) - topLeftPos) * tileSize
            x = textPos.x
            y = textPos.y
            defaultSize = 50
            graphics.gui.drawText(str(self.divisor), x, y, int(defaultSize * scale), (62, 62, 62), "Encode Sans Bold")
        
    def copy(self):
        return Tile(self.pos, self.color, self.appearedTime, self.disappearTime, self.type, self.divisor)