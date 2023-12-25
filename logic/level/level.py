from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *

class Level:
    def __init__(self, tiles, appearLength, disappearLength):
        self.win = None

        self.tiles = tiles
        self.appearLength = appearLength
        self.disappearLength = disappearLength
        self.pos = Vector2(0, 0)
        
        self.player = Player(Vector2(0, 0))
    
    def update(self, win, time):
        self.win = win
        
        self.player.updatePos(time)
        
        for i in self.tiles:
            i.draw(win, self.player.visiblePos, self.appearLength, self.disappearLength, time, levelPos = self.pos)

        self.player.draw(win)
        
    def move(self, delta):
        self.pos += delta