from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *

class Level:
    def __init__(self, tiles, appearLength, disappearLength):
        self.win = None
        self.appearLength = appearLength
        self.disappearLength = disappearLength
        
        tileEvents = []
        for tile in tiles:
            startTime = tile.appearedTime - self.appearLength
            endTime = tile.disappearTime + self.disappearLength
            callback = lambda t, win, playerPos, tile=tile: tile.draw(win, playerPos, self.appearLength, self.disappearLength, t + tile.appearedTime - appearLength)
            data = tile
            tileEvents.append(AnimEvent(startTime, endTime, callback, data))
        self.tileAnim = Animation(tileEvents, 0)
        self.pos = Vector2(0, 0)
        
        self.player = Player(Vector2(0, 0), 0)
        
    def start(self, time):
        self.tileAnim.restart(time)
    
    def draw(self, win, time):        
        pos = self.player.calculatePos(self, time)
        if isinstance(pos, Vector2):
            self.tileAnim.updateTime(time, win, self.player.calculateVisiblePos(self, time)) 
        else:
            return "Dead"
        self.player.draw(win)
        
    def move(self, delta):
        self.pos += delta
        
    def getTileAt(self, pos, time):
        for i in self.tileAnim.tree.at(time):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
            