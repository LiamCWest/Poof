from objects.tiles.tile import Tile
from utils.vector2 import Vector2

class Board():
    def __init__(self, pos, size, tileSize, color):
        self.pos = pos
        self.size = size
        self.tileSize = tileSize
        self.color = color
        self.tiles = []
        self.createTiles()
        
    def createTiles(self):
        for y in range(self.size.y):
            for x in range(self.size.x):
                self.tiles.append(Tile(self, Vector2(x, y), self.tileSize, self.color))
                
    def draw(self, win):
        for tile in self.tiles:
            tile.draw(win)
            
    def move(self, direction):
        self.pos += direction.multiply(self.tileSize)
        for tile in self.tiles:
            tile.updatePos()