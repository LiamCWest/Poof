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
    def __init__(self, tiles, appearLength, disappearLength, songPath, timingPoints, playerStartPos = None, playerStartTime = None):
        self.win = None
        self.appearLength = appearLength
        self.disappearLength = disappearLength
        self.tiles = tiles
        
        tileEvents = [self.createEventFromTile(tile) for tile in tiles]
        self.tileAnim = Animation(tileEvents, 0)
        self.pos = Vector2(0, 0)
        self.tileSize = Vector2(50, 50)
        self.grid = self.genGrid(Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1]), 5)
        
        self.playerStartPos = playerStartPos
        self.playerStartTime = playerStartTime
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime)
        
        self.songPath = songPath
        self.timingPoints = timingPoints
        songPlayer.load(self.songPath, self.timingPoints)
        songPlayer.pause()
    
    def createEventFromTile(self, tile):
        startTime = tile.appearedTime - self.appearLength
        endTime = tile.disappearTime + self.disappearLength
        callback = lambda t, win, topLeftPos, tileSize, tile=tile: tile.draw(win, topLeftPos, tileSize, self.appearLength, self.disappearLength, t + tile.appearedTime - self.appearLength)
        data = tile
        return AnimEvent(startTime, endTime, callback, data)
    
    def addTile(self, tile):
        self.tiles.append(tile)
        self.tileAnim.addEvent(self.createEventFromTile(tile))
    
    def createPlayer(self, playerStartPos, playerStartTime):
        if playerStartPos is not None and playerStartTime is not None:
            return Player(playerStartPos, playerStartTime)
        return None
    
    def restart(self):
        self.pos = Vector2(0, 0)
        
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime)
        
        songPlayer.play()
        self.tileAnim.restart(songPlayer.getPos())        
    
    def draw(self, win, timeSourceTime, topLeftPos, tileSize, drawPlayer = True):
        self.tileAnim.updateTime(timeSourceTime, win, topLeftPos, tileSize)
        if self.player is not None and drawPlayer:
            self.player.draw(win)
            
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
        tileValues = [tile.toValues() for tile in self.tiles]
        for tile in tileValues:
            noV2sTiles.append([tile[0].toTuple(), tile[1], tile[2], tile[3], tile[4]])
            
        timingPoints = []
        for timingPoint in self.timingPoints:
            timingPoints.append(timingPoint.toValues())
            
        levelData = {
            "tiles": noV2sTiles,
            "appearLength": self.appearLength,
            "disappearLength": self.disappearLength,
            "songPath": self.songPath,
            "timingPoints": timingPoints,
            }
        
        signature = signData(levelData)
        
        with open('level_data.json', 'w') as file:
            json.dump({"data": levelData, "signature": signature}, file)
            
    def screenPosToTilePos(self, screenPos, topLeftPos):
        return screenPos / self.tileSize + topLeftPos
    
    def screenPosToRoundedTilePos(self, screenPos, topLeftPos):
        tilePos = screenPos / self.tileSize + topLeftPos
        return Vector2(math.floor(tilePos.x), math.floor(tilePos.y))
    
    def tilePosToScreenPos(self, tilePos, topLeftPos):
        return self.tileSize * (topLeftPos - tilePos)

def signData(data):
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return signature

def checkSignature(data, signature):
    return signature == signData(data)