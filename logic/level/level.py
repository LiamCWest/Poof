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
            callback = lambda t, tile=tile: tile.draw(self.win, self.player.visiblePos, self.appearLength, self.disappearLength, t + tile.appearedTime - appearLength)
            data = tile
            tileEvents.append(AnimEvent(startTime, endTime, callback, data))
        self.tileAnim = Animation(tileEvents, 0)

        self.appearLength = appearLength
        self.disappearLength = disappearLength
        self.pos = Vector2(0, 0)
        
        self.player = Player(Vector2(0, 0))
        
    def start(self, time):
        self.tileAnim.restart(time)
    
    def update(self, win, time):
        self.win = win
        
        self.player.updateVisiblePos(time)
        self.tileAnim.updateTime(time)
        self.player.draw(win)
        
    def move(self, delta):
        self.pos += delta