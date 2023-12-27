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
    def __init__(self, tiles, appearLength, disappearLength, songPath):
        self.win = None
        self.songPath = songPath
        songPlayer.load(self.songPath, [TimingPoint(2.108, 170, TimeSignature(4, 4))])
        self.playing = False
        self.tileValues = tiles
        self.tiles = self.genTiles(self.tileValues)
        tileEvents = []
        for tile in self.tiles:
            startTime = tile.appearedTime - appearLength
            endTime = tile.disappearTime + disappearLength
            callback = lambda t, tile=tile: tile.draw(self.win, self.player.visiblePos, self.appearLength, self.disappearLength, t + tile.appearedTime - appearLength)
            data = tile
            tileEvents.append(AnimEvent(startTime, endTime, callback, data))
        self.tileAnim = Animation(tileEvents, 0)

        self.appearLength = appearLength
        self.disappearLength = disappearLength
        self.pos = Vector2(0, 0)
        self.tileSize = Vector2(50, 50)
        self.grid = self.genGrid(Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1]), 5)
        
        self.player = Player(Vector2(0, 0))
        
    def genTiles(self, tiles):
        outTiles = []
        for tile in tiles:
            outTiles.append(Tile(tile[0], tile[1], tile[2], tile[3], tile[4]))
        return outTiles
        
    def addTile(self, tile):
        tile[0] -= self.player.offset
        self.tileValues.append(tile)
        tile = self.genTiles([tile])[0]
        self.tiles.append(tile)
        startTime = tile.appearedTime - self.appearLength
        endTime = tile.disappearTime + self.disappearLength
        callback = lambda t, tile=tile: tile.draw(self.win, self.player.visiblePos, self.appearLength, self.disappearLength, t + tile.appearedTime - self.appearLength)
        data = tile
        self.tileAnim.addEvent(AnimEvent(startTime, endTime, callback, data))
        
    def start(self, time):
        self.tileAnim.restart(time)
        
    def play(self):
        songPlayer.play()
        self.playing = True
    
    def draw(self, win, time, showPlayer = True, showGrid = False):
        self.win = win
        
        self.player.updateVisiblePos(time)
        self.tileAnim.updateTime(time)
        if showPlayer: self.player.draw(win)
        if showGrid: self.drawGrid(win)
        
    def move(self, delta):
        self.pos += delta
        for tile in self.tiles:
            tile.levelPos = self.pos
        self.player.levelPos = self.pos
                
        for line in self.grid:
            line.pos = ((line.pos + delta) % self.tileSize) - self.tileSize
        
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