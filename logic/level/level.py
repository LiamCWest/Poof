from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *
from utils.polygon import Polygon
import graphics.gui as gui
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimeSignature, TimingPoint
from objects.tile import Tile
import json
import hashlib

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
        self.tileSize = Vector2(50, 50)
        self.grid = self.genGrid(Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1]), 5)
        
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
        for tile in self.tiles:
            tile.levelPos = self.pos
        self.player.levelPos = self.pos
                
        for line in self.grid:
            line.pos = ((line.pos + delta) % self.tileSize) - self.tileSize
            
    def getTileAt(self, pos, levelTime):
        for i in self.tileAnim.tree.at(levelTime):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
        
    def genGrid(self, size, lineSize):
        size += self.tileSize
        width = math.ceil(size.x/self.tileSize.x)
        height = math.ceil(size.y/self.tileSize.y)
        columns = []
        for x in range(width):
            columns.append(Polygon([(x*self.tileSize.x, 0), (x*self.tileSize.x + lineSize, 0), (x*self.tileSize.x + lineSize, size.y), (x*self.tileSize.x, size.y)]))
            
        rows = []
        for y in range(height):
            rows.append(Polygon([(0, y*self.tileSize.y), (size.x, y*self.tileSize.y), (size.x, y*self.tileSize.y + lineSize), (0, y*self.tileSize.y + lineSize)]))
        return columns + rows
    
    def drawGrid(self, win):
        for polygon in self.grid:
            polygon.draw(win)
            
    def save(self):
        noV2sTiles = []
        for tile in self.tileValues:
            noV2sTiles.append([tile[0].toTuple(), tile[1], tile[2], tile[3], tile[4]])
            
        levelData = {
            "tiles": noV2sTiles,
            "appearLength": self.appearLength,
            "disappearLength": self.disappearLength,
            "songPath": self.songPath,
            }
        
        signature = signData(levelData)
        
        with open('level_data.json', 'w') as file:
            json.dump({"data": levelData, "signature": signature}, file)

def signData(data):
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return signature

def checkSignature(data, signature):
    return signature == signData(data)