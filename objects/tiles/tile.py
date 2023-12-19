import pygame

from objects.gameObject import GameObject
from utils.vector2 import Vector2

class Tile(GameObject):
    def __init__(self, board, pos, size, color, image = None):
        self.board = board
        self.relPos = pos
        x = self.relPos.x * board.tileSize + round(board.tileSize*self.relPos.x*0.1) + board.pos.x
        y = self.relPos.y * board.tileSize + round(board.tileSize*self.relPos.y*0.1) + board.pos.y
        GameObject.__init__(self, Vector2(x,y), size, size, color, image)
        
    def updatePos(self):
        x = self.relPos.x * self.board.tileSize + round(self.board.tileSize*self.relPos.x*0.1) + self.board.pos.x
        y = self.relPos.y * self.board.tileSize + round(self.board.tileSize*self.relPos.y*0.1) + self.board.pos.y
        self.pos = Vector2(x,y)