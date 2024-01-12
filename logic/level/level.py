# external imports
import hashlib
import json

# internal imports
import graphics.gui as gui
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimeSignature, TimingPoint
from utils.vector2 import Vector2
from utils.polygon import Polygon
from objects.player import Player
from objects.tile import Tile
from graphics.animation import *

class Level:
    deathTimeBuffer = 0.5
    def __init__(self, tiles, appearLength, disappearLength, songPath, timingPoints, playerStartPos = None, playerStartTime = None):
        self.win = None
        self.appearLength = appearLength
        self.disappearLength = disappearLength
        
        tileEvents = [self.createEventFromTile(tile) for tile in tiles]
        self.tileAnim = Animation(tileEvents, 0)
        self.pos = Vector2(0, 0)
        self.tileSize = Vector2(100, 100)
        
        self.playerStartPos = playerStartPos
        self.playerStartTime = playerStartTime
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime)
        
        self.songPath = songPath
        self.timingPoints = timingPoints
        songPlayer.load(self.songPath)
    
    def createEventFromTile(self, tile):
        startTime = tile.appearedTime - self.appearLength
        endTime = tile.disappearTime + self.disappearLength
        callback = lambda t, win, topLeftPos, tileSize, tile=tile: tile.draw(win, topLeftPos, tileSize, self.appearLength, self.disappearLength, t + tile.appearedTime - self.appearLength)
        data = tile
        return AnimEvent(startTime, endTime, callback, data)
    
    def addTile(self, tile):
        self.tileAnim.addEvent(self.createEventFromTile(tile))
        
    def removeTileAt(self, pos, levelTime):
        for i in self.tileAnim.tree.at(levelTime):
            tile = i.data[1]
            if tile.pos == pos:
                self.tileAnim.tree.remove(i)
    
    def createPlayer(self, playerStartPos, playerStartTime):
        if playerStartPos is not None and playerStartTime is not None:
            return Player(playerStartPos, playerStartTime)
        return None
    
    def restart(self):
        self.pos = Vector2(0, 0)
        
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime)
        
        songPlayer.seek(0)
        songPlayer.unpause()
        self.tileAnim.restart(songPlayer.getPos())        
    
    def draw(self, win, timeSourceTime, topLeftPos, tileSize, drawPlayer = False, freezeTilesOnDeath = False, playerState = None, drawGrid = False, gridLineThickness = 2):            
        if drawPlayer and freezeTilesOnDeath and playerState.deathTime is not None and playerState.deathTime < timeSourceTime:
            levelTime = playerState.deathTime
        else:
            levelTime = timeSourceTime
        
        self.tileAnim.updateTime(levelTime, win, topLeftPos, tileSize)
        
        if self.player is not None and drawPlayer:
            self.player.draw(win, playerState)
        
        if drawGrid:
            ltHalf = gridLineThickness / 2
            screenSize = Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1])
            topLeftMod = self.tilePosToScreenPos(topLeftPos, Vector2(0, 0)) % tileSize
            
            gridWidth = screenSize.x + tileSize.x
            gridHeight = screenSize.y + tileSize.y
            for i in range(math.floor(screenSize.x / tileSize.x) + 2):
                pos = topLeftMod - tileSize + (Vector2(i, 0) * tileSize)
                polygon1 = Polygon.fromRect((pos.x - ltHalf, pos.y - ltHalf, gridLineThickness, gridHeight))
                polygon1.draw(win)
                
            for i in range(math.floor(screenSize.y / tileSize.y) + 2):
                pos = topLeftMod - tileSize + (Vector2(0, i) * tileSize)
                polygon1 = Polygon.fromRect((pos.x - ltHalf, pos.y - ltHalf, gridWidth, gridLineThickness))
                polygon1.draw(win)
            
    def getTileAt(self, pos, levelTime):
        for i in self.tileAnim.tree.at(levelTime):
            tile = i.data[1]
            if tile.pos == pos:
                return tile
        return None
    
    def getTilesOverlapping(self, pos, startTime, endTime):
        tiles = []
        for i in self.tileAnim.tree.overlap(startTime, endTime):
            tile = i.data[1]
            if tile.pos == pos:
                tiles.append(tile)
        tiles.sort(key=lambda tile: tile.appearedTime)
        return tiles
            
    def isTileValid(self, tile, oldTile):
        if tile.appearedTime < 0 or tile.disappearTime < 0 or tile.appearedTime > songPlayer.getSongLength():
            return False
        if tile.appearedTime > tile.disappearTime:
            return False
        overlapping = self.tileAnim.tree.overlap(tile.appearedTime, tile.disappearTime)
        for i in overlapping:
            if i.data[1].pos == tile.pos and i.data[1] != oldTile:
                return False
        return True

    def save(self, levelFile):
        tileValues = [event.data[1].toValues() for event in self.tileAnim.tree]
        noV2sTiles = [[tile[0].toTuple(), tile[1], tile[2], tile[3], tile[4], tile[5]] for tile in tileValues]
    
        timingPoints = [point.toValues() for point in self.timingPoints]
            
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
    
    def getEndTime(self):
        return math.nextafter(self.tileAnim.tree.end(), float("-inf")) - self.disappearLength
    
    def getEndPositions(self):
        endIntervals =  self.tileAnim.tree.at(math.nextafter(self.tileAnim.tree.end(), float("-inf")))
        endTiles = [i.data[1].pos for i in endIntervals]
        return endTiles
    
    @classmethod
    def fromFile(cls, levelFile):
        with open(levelFile, 'r') as file:
            saved_data = json.load(file)
            loaded_data = saved_data['data']
            saved_signature = saved_data['signature']
            if not checkSignature(loaded_data, saved_signature):
                print("Level file corrupted")
                return None
            tiles = loaded_data['tiles']
            tilesV2 = [Tile(Vector2.from_tuple(tile[0]), tile[1], tile[2], tile[3], tile[4], tile[5]) for tile in tiles]
            appearLength = loaded_data['appearLength']
            disappearLength = loaded_data['disappearLength']
            songPath = loaded_data['songPath']
            timingPointsVals = loaded_data['timingPoints']
            timingPoints = [TimingPoint(timingPoint[0], timingPoint[1], TimeSignature(timingPoint[2], timingPoint[3])) for timingPoint in timingPointsVals]
            playerStartPos = Vector2.from_tuple(loaded_data['playerStartPos'])
            playerStartTime = loaded_data['playerStartTime']
            level = cls(tilesV2, appearLength, disappearLength, songPath, timingPoints, playerStartPos, playerStartTime)
            return level

def signData(data):
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return signature

def checkSignature(data, signature):
    return signature == signData(data)

def rangeOverlapsWithRange(range1, range2):
    return range1[0] <= range2[1] and range2[0] <= range1[1]