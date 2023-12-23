from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *

class Level:
    def __init__(self, tiles, appearLength, disappearLength):
        self.win = None

        self.tiles = tiles
        self.appearLength = appearLength
        self.disappearLength = disappearLength
        
        self.player = Player(Vector2(0, 0))
    
    def update(self, win, time):
        self.win = win
        
        for i in self.tiles:
            i.draw(win, self.player.pos, self.appearLength, self.disappearLength, time)

        self.player.draw(win)