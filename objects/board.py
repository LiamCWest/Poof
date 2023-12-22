from objects.tiles.tile import Tile
from utils.vector2 import Vector2
from objects.tiles.platform import Platform
from objects.tiles.rest import Rest
from graphics.animation import *
import input.input as input

class Board:
    moveLength = 0.15
    def __init__(self, pos, size, tileSize, color):
        self.pos = pos.add(tileSize*0.1)
        self.size = size
        self.tileSize = tileSize
        self.color = color
        self.tiles = []
        self.targetPos = self.pos
        self.moveStartedTime = input.getRealTime()
        self.moveStartedPos = self.pos
        self.animations = []
        
        moveEvent = AnimEvent(0, self.moveLength, self.updatePos)
        self.moveAnim = Animation([moveEvent], self.moveStartedTime, "oneShot", self.moveLength)
        
        self.createTiles()
        
    def createTiles(self):
        for y in range(self.size.y):
            for x in range(self.size.x):
                r = (x+y) % 3
                if r == 0:
                    self.tiles.append(Platform(self, Vector2(x, y), self.tileSize, self.color))
                if r == 1:
                    self.tiles.append(Tile(self, Vector2(x, y), self.tileSize, self.color))
                if r == 2:
                    self.tiles.append(Rest(self, Vector2(x, y), self.tileSize, self.color))
                
    def draw(self, win):
        for tile in self.tiles:
            if tile.pos.x >= -tile.width and tile.pos.x <= win.get_width() and tile.pos.y >= -tile.height and tile.pos.y <= win.get_height():
                tile.draw(win)
    
    def updatePos(self, currentTime):
        self.pos.x = easeOutPow(self.moveStartedPos.x, self.targetPos.x, 0, self.moveLength, 2, currentTime)
        self.pos.y = easeOutPow(self.moveStartedPos.y, self.targetPos.y, 0, self.moveLength, 2, currentTime)
    
    def move(self, direction):
        self.targetPos += direction.multiply(round(self.tileSize*1.1))  # set target position
        self.moveStartedPos = self.pos.copy()
        self.moveAnim.restart(input.getRealTime())

    def update(self):
        if self.pos != self.targetPos:
            self.moveAnim.updateTime(input.getRealTime())
            
            for tile in self.tiles:
                tile.updatePos()
        self.updateAnimations()
                
    def addAnimation(self, anim):
        self.animations.append(anim)
        
    def removeAnimation(self, anim):
        self.animations.remove(anim)
        
    def updateAnimations(self):
        for anim in self.animations:
            anim.updateTime(input.getRealTime())