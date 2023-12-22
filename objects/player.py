import math

from objects.gameObject import GameObject
from utils.vector2 import Vector2

class Player(GameObject):
    def __init__(self, board, pos, size, color = (0,0,0), imageName = "player"):
        self.board = board
        self.relPos = pos
        self.scale = 0.8
        self.width = size * self.scale
        self.height = size * self.scale
        self.updatePos()
        GameObject.__init__(self, self.pos, self.width, self.height, color, imageName)
        
    def updatePos(self):
        x = self.board.tileSize*self.relPos.x*1.1 + (self.board.tileSize/2 - self.width/2) + self.board.pos.x
        y = self.board.tileSize*self.relPos.y*1.1 + (self.board.tileSize/2 - self.height/2) + self.board.pos.y
        self.pos = Vector2(x,y)

    def move(self, direction):
        self.relPos += direction