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
        
    def removeTile(self, tile):
        self.tiles.remove(tile)
        self.tileAnim.removeEvent(self.createEventFromTile(tile))
    
    def createPlayer(self, playerStartPos, playerStartTime):
        if playerStartPos is not None and playerStartTime is not None:
            return Player(playerStartPos, playerStartTime)
        return None
    
    def getTileByPos(self, pos):
        for tile in self.tiles:
            if tile.pos == pos:
                return tile
        return None
    
    def restart(self):
        self.pos = Vector2(0, 0)
        
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime)
        
        songPlayer.play()
        self.tileAnim.restart(songPlayer.getPos())        
    
    def draw(self, win, timeSourceTime, topLeftPos, tileSize, drawPlayer = False, playerPos = None, visiblePos = None, drawGrid = False, gridLineThickness = 2):
        self.tileAnim.updateTime(timeSourceTime, win, topLeftPos, tileSize)
        
        if self.player is not None and drawPlayer:
            self.player.draw(win, playerPos, visiblePos, timeSourceTime)
        
        if drawGrid:
            ltHalf = gridLineThickness / 2
            screenSize = Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1])
            topLeftMod = self.tilePosToScreenPos(topLeftPos, Vector2(0, 0)) % tileSize
            
            gridWidth = screenSize.x + tileSize.x
            gridHeight = screenSize.y + tileSize.y
            for i in range(math.floor(screenSize.x / tileSize.x) + 2):
                pos = topLeftMod - tileSize + (Vector2(i, 0) * tileSize)
                polygon1 = Polygon([(pos.x - ltHalf, pos.y), (pos.x + ltHalf, pos.y), (pos.x + ltHalf, pos.y + gridHeight), (pos.x - ltHalf, pos.y + gridHeight)])
                polygon1.draw(win)
                
            for i in range(math.floor(screenSize.y / tileSize.y) + 2):
                pos = topLeftMod - tileSize + (Vector2(0, i) * tileSize)
                polygon1 = Polygon([(pos.x, pos.y - ltHalf), (pos.x, pos.y + ltHalf), (pos.x + gridWidth, pos.y + ltHalf), (pos.x + gridWidth, pos.y - ltHalf)])
                polygon1.draw(win)
            
    def getTileAt(self, pos, levelTime):
        for i in self.tileAnim.tree.at(levelTime):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
            
    def save(self, levelFile):
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
            "playerStartPos": self.playerStartPos.toTuple(),
            "playerStartTime": self.playerStartTime
            }
        
        signature = signData(levelData)
        
        with open(levelFile, 'w') as file:
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