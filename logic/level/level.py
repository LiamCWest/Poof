from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *

class Level:
    def __init__(self, tiles, appearLength, disappearLength):
        self.win = None
        
        tileEvents = []
        for tile in tiles:
            startTime = tile.appearedTime - appearLength
            endTime = tile.disappearTime + disappearLength
            callback = lambda t, tile=tile: tile.draw(self.win, self.playerPos, self.appearLength, self.disappearLength, t + tile.appearedTime - appearLength)
            data = tile
            tileEvents.append(AnimEvent(startTime, endTime, callback, data))
        self.tileAnim = Animation(tileEvents, 0)

        self.appearLength = appearLength
        self.disappearLength = disappearLength
        self.pos = Vector2(0, 0)
        
        self.playerPos = Vector2(0, 0)
        
        self.player = Player(Vector2(0, 0))
        
    def start(self, time):
        self.tileAnim.restart(time)
    
    def draw(self, win, time):
        self.win = win
        
        pos = self.player.calculatePos(self, time, 0)
        if isinstance(pos, Vector2):
            self.playerPos = self.player.calculateVisiblePos(self, time, 0)
        else:
            return "Dead"
        self.tileAnim.updateTime(time)
        self.player.draw(win)
        
    def move(self, delta):
        self.pos += delta
        
    def getTileAt(self, pos, time):
        for i in self.tileAnim.tree.at(time):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
            