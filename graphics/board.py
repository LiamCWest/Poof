from objects.tiles.tile import Tile
from utils.vector2 import Vector2
from objects.tiles.platform import Platform
from objects.tiles.rest import Rest

class Board:
    def __init__(self, pos, size, tileSize, color):
        self.pos = pos.add(tileSize*0.1)
        self.size = size
        self.tileSize = tileSize
        self.color = color
        self.tiles = []
        self.targetPos = self.pos
        self.velocity = 1
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
            
    def move(self, direction):
        self.targetPos += direction.multiply(round(self.tileSize*1.1))  # set target position

    def update(self):
        if self.pos != self.targetPos:
            direction = (self.targetPos - self.pos).normalize()
            self.pos += direction.multiply(self.velocity)
            if (self.targetPos - self.pos).length() < self.velocity:
                self.pos = self.targetPos
            for tile in self.tiles:
                tile.updatePos()