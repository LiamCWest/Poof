from utils.vector2 import Vector2
from utils.polygon import Polygon
from ui.text import Text

import pygame

class Toolbar:
    def __init__(self, gridSize, pos, width, height):
        self.gridSize = gridSize
        self.objects = []
        self.grid = [[None for i in range(gridSize.x)] for j in range(gridSize.y)]
        self.pos = pos
        self.width = width
        self.height = height
        
    def addOption(self, option, grid):
        self.grid[grid.y][grid.x] = option
        self.objects.append(option)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.getRect())
        for i in range(self.gridSize.x):
            for j in range(self.gridSize.y):
                if self.grid[j][i]:
                    self.grid[j][i].draw(screen, self.pos + Vector2(i*self.width/self.gridSize.x, j*self.height/self.gridSize.y))
    
    def update(self):
        for i in range(self.gridSize.x):
            for j in range(self.gridSize.y):
                if self.grid[j][i]:
                    self.grid[j][i].update(self.pos + Vector2(i*self.width/self.gridSize.x, j*self.height/self.gridSize.y))
                    
    def getRect(self):
        return (self.pos.x,
                self.pos.y,
                self.width,
                self.height)

class ToolbarOption:
    def __init__(self, name, baseObj):
        self.name = name
        self.baseObj = baseObj
        
    def draw(self, screen, pos):
        if type(self.baseObj) == list:
            for i, obj in enumerate(self.baseObj):
                if type(obj) != Text: obj.draw(screen, pos = pos)
                else: obj.draw(pos = pos, win = screen)
        else:
            if type(self.baseObj) != Text: self.baseObj.draw(screen, pos = pos)
            else: self.baseObj.draw(pos = pos)
        
    def update(self, pos):
        if type(self.baseObj) == list:
            for i, obj in enumerate(self.baseObj):
                if type(obj) not in [Text, Polygon]: 
                    obj.update(pos)
        else:
            self.baseObj.update(pos)