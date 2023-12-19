from objects.tiles.tile import Tile
from utils.vector2 import Vector2

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
                self.tiles.append(Tile(self, Vector2(x, y), self.tileSize, self.color, image = None))
                
    def draw(self, win):
        for tile in self.tiles:
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