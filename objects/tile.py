# external imports
import pygame #pygame

# internal imports
import graphics.gui #for drawing text
from images import images #for getting images

class Tile: #a tile in a level
    def __init__(self, pos, color, appearedTime = 0, disappearTime = 0, type = "platform", divisor = None): #constructor
        self.pos = pos #the tile's position
        self.color = color #the tile's color (unused)
        self.appearedTime = appearedTime #the time the tile is fully appeared
        self.disappearTime = disappearTime #the time the tile starts disappearing
        self.type = type #the type of tile
        self.divisor = divisor #the divisor of the glide tile
    
    def getTypeImage(self): #gets the image for the tile's type
        if self.type == "platform": #if the tile is a platform
            return images.images["platform"] #return the platform image
        elif self.type == "glide": #if the tile is a glide tile
            return images.images["glide"] #return the glide tile image
        elif self.type == "rest": #if the tile is a rest tile
            return images.images["rest"] #return the rest tile image
        else: #if the tile is a glide path tile
            return images.images["glidePath"] #return the glide path tile image
    
    def getScaleFromAppearAnimTime(self, timeIntoAppearAnim, appearLength): #get scale of tile from time into appear animation
        return timeIntoAppearAnim / appearLength #lerp
    
    def getScaleFromDisappearAnimTime(self, timeIntoDisappearAnim, disappearLength): #get scale of tile from time into disappear animation
        return 1 - (timeIntoDisappearAnim / disappearLength) #lerp

    def draw(self, win, topLeftPos, tileSize, appearLength, disappearLength, time): #draws the tile
        if time < self.appearedTime - appearLength: #if before tile appears
            scale = 0 #scale is 0
        elif time <= self.appearedTime: #if tile is appearing
            timeIntoAppearAnim = time - (self.appearedTime - appearLength) #get time into appear animation
            scale = self.getScaleFromAppearAnimTime(timeIntoAppearAnim, appearLength) #get scale from time into appear animation
        elif time < self.disappearTime: #if tile is fully appeared
            scale = 1 #scale is 1
        elif time <= self.disappearTime + disappearLength: #if tile is disappearing
            timeIntoDisappearAnim = time - self.disappearTime #get time into disappear animation
            scale = self.getScaleFromDisappearAnimTime(timeIntoDisappearAnim, disappearLength) #get scale from time into disappear animation
        else: #if after tile disappears
            scale = 0 #scale is 0
        scale **= 5 #raise scale to 5th power for a nice exponential animation
        
        pos = ((self.pos - topLeftPos) * tileSize + tileSize.multiply(1 - scale).divide(2)).toTuple() #get the screen position of tile from level pos
        win.blit(pygame.transform.scale(self.getTypeImage(), tileSize.multiply(scale).toTuple()), pos) #draw the tile to the window
        
        if self.type == "glide": #if the tile is a glide tile
            textPos = (self.pos.add(0.5) - topLeftPos) * tileSize #get the screen position of the text from level pos
            x = textPos.x #get x
            y = textPos.y #get y
            defaultSize = 50 #the default font size of the text
            graphics.gui.drawText(str(self.divisor), x, y, int(defaultSize * scale), (62, 62, 62), "Encode Sans Bold") #draw the text to the window
        
    def copy(self): #returns a copy of the tile
        return Tile(self.pos, self.color, self.appearedTime, self.disappearTime, self.type, self.divisor) #reconstruct
    
    def toValues(self): #converts tile to values for serialization
        return [self.pos, self.color, self.appearedTime, self.disappearTime, self.type, self.divisor] #return values