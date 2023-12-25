from utils.vector2 import Vector2
from objects.player import Player
from graphics.animation import *
from utils.polygon import Polygon
import graphics.gui as gui
import pygame

class Level:
    def __init__(self, tiles, appearLength, disappearLength):
        self.win = None
        self.tiles = tiles
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
        self.tileSize = Vector2(50, 50)
        self.grid = self.genGrid(Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1]), 5)
        
        self.player = Player(Vector2(0, 0))
        
    def addTile(self, tile):
        self.tiles.append(tile)
        startTime = tile.appearedTime - self.appearLength
        endTime = tile.disappearTime + self.disappearLength
        callback = lambda t, tile=tile: tile.draw(self.win, self.player.visiblePos, self.appearLength, self.disappearLength, t + tile.appearedTime - self.appearLength)
        data = tile
        self.tileAnim.addEvent(AnimEvent(startTime, endTime, callback, data))
        
    def start(self, time):
        self.tileAnim.restart(time)
    
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
            line.move(delta)
        
    def genGrid(self, size, lineSize):
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