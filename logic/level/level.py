from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *
from logic.song import songPlayer
from logic.song.timingPoints import TimingPoint, TimeSignature

class Level:
    deathTimeBuffer = 0.25
    def __init__(self, tiles, appearLength, disappearLength, songPath, timingPoints):
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
        
        self.songPath = songPath
        self.timingPoints = timingPoints
        songPlayer.load(self.songPath, self.timingPoints)
        
    def start(self):
        self.pos = Vector2(0, 0)
        self.player = Player(Vector2(0, 0), 0)
        
        songPlayer.play()
        self.tileAnim.restart(songPlayer.getPos())
    
    def draw(self, win, timeSourceTime):        
        pos = self.player.calculatePos(self, timeSourceTime)
        if isinstance(pos, Vector2):
            self.tileAnim.updateTime(timeSourceTime, win, self.player.calculateVisiblePos(self, timeSourceTime))
            self.player.draw(win)
        else:
            if pos[1] + self.deathTimeBuffer < timeSourceTime: #A buffer so you don't die unfairly if you have input delay
                self.start()
            else:
                self.tileAnim.updateTime(timeSourceTime, win, self.player.calculateVisiblePos(self, timeSourceTime))
        
    def move(self, delta):
        self.pos += delta
        
    def getTileAt(self, pos, levelTime):
        for i in self.tileAnim.tree.at(levelTime):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
            