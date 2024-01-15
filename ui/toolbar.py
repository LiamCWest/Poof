# external imports
import pygame # import pygame library

# internal imports
from utils.vector2 import Vector2 # import Vector2 class from utils/vector2.py
from utils.polygon import Polygon # import Polygon class from utils/polygon.py
from ui.text import Text # import Text class from ui/text.py

# Toolbar class
class Toolbar:
    def __init__(self, gridSize, pos, width, height): # constructor
        self.gridSize = gridSize # gridSize is a Vector2 object
        self.objects = [] # objects is a list of ToolbarOption objects
        self.grid = [[None for i in range(gridSize.x)] for j in range(gridSize.y)] # grid is a 2d list of ToolbarOption objects
        self.pos = pos # pos is a Vector2 object
        self.width = width # width is a number
        self.height = height # height is a number
        
    def addOption(self, option, grid): # add an option to the toolbar
        self.grid[grid.y][grid.x] = option # add the option to the grid
        self.objects.append(option) # add the option to the objects list
        
    def draw(self, screen): # draw the toolbar
        pygame.draw.rect(screen, (0,0,0), self.getRect()) # draw the toolbar background
        for i in range(self.gridSize.x): # loop through the grid rows
            for j in range(self.gridSize.y): # loop through the grid columns
                if self.grid[j][i]: # if the grid cell is not empty
                    self.grid[j][i].draw(screen, self.pos + Vector2(i*self.width/self.gridSize.x, j*self.height/self.gridSize.y)) # draw the object in the grid cell with offsets based on the grid cell's position
    
    def update(self): # update the toolbar
        for i in range(self.gridSize.x): # loop through the grid rows
            for j in range(self.gridSize.y): # loop through the grid columns
                if self.grid[j][i]: # if the grid cell is not empty
                    self.grid[j][i].update(self.pos + Vector2(i*self.width/self.gridSize.x, j*self.height/self.gridSize.y)) # update the object in the grid cell with offsets based on the grid cell's position
                    
    def getRect(self): # get the toolbar's rect
        return (self.pos.x,
                self.pos.y,
                self.width,
                self.height) # return the toolbar's rect

class ToolbarOption: # ToolbarOption class
    def __init__(self, name, baseObj): # constructor
        self.name = name # name is a string
        self.baseObj = baseObj # baseObj is the object being displayed in the toolbar
        
    def draw(self, screen, pos): # draw the toolbar option
        if type(self.baseObj) == list: # if the baseObj is a list of objects
            for i, obj in enumerate(self.baseObj): # loop through the list
                # text objects draw differently than other objects
                if type(obj) != Text: obj.draw(screen, pos = pos) # if the object is not a Text object, draw it with correct values
                else: obj.draw(pos = pos, win = screen) # if the object is a Text object, draw it with correct values
        else: # if the baseObj is not a list of objects
            # text objects draw differently than other objects
            if type(self.baseObj) != Text: self.baseObj.draw(screen, pos = pos) # if the object is not a Text object, draw it with correct values
            else: self.baseObj.draw(pos = pos) # if the object is a Text object, draw it with correct values
        
    def update(self, pos): # update the toolbar option
        if type(self.baseObj) == list: # if the baseObj is a list of objects
            for i, obj in enumerate(self.baseObj): # loop through the list
                # text and polygon objects do not update
                if type(obj) not in [Text, Polygon]:  # if the object is not a Text or Polygon object
                    obj.update(pos) # update the object with correct values
        else: # if the baseObj is not a list of objects
            self.baseObj.update(pos) # update the object with correct values