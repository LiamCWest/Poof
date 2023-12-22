from Poof.objects import tile
from objects.board import Board
from objects.tiles import rest, wall, platform
from utils.vector2 import Vector2
from graphics.animation import *
from input import input

class LevelEvent:
    def __init__(self, tile, appearedTime, disappearedTime):
        self.tile = tile
        self.appearedTime = appearedTime
        self.disappearedTime = disappearedTime


class Level(Board):
    def __init__(self, events, appearTime, disappearTime):
        self.events = events
        self.appearTime = appearTime
        self.disappearTime = disappearTime
        animEvents = [LevelEvent(i.appearedTime - appearTime, i.appearedTime - appearTime, i.tile.appear) for i in events] + [
            LevelEvent(LevelEvent(i.disappearedTime - appearTime, i.disappearedTime - appearTime, i.tile.disappear) for i in events)]
        self.addAnimation(Animation(animEvents, input.getRealTime()))
        super().__init__(Vector2(0, 0), Vector2(24, 20), 50, (25, 25, 25))

e1 = LevelEvent(platform.Platform())