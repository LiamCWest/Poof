from images import images
import pygame
from utils.vector2 import Vector2
from graphics.animation import *

class Player:
    offset = Vector2(5, 4)
    moveTime = 0.1
    def __init__(self, pos):        
        self.moves = [] #Tuple of (diff, time)
        
    def draw(self, win):
        size = Vector2(50, 50)
        img = images.images["player"]
        
        win.blit(pygame.transform.scale(img, size.toTuple()), (size * self.offset).toTuple())
        
    def move(self, diff, time):
        self.moves.append((diff, time))
        
    def calculatePos(self, level, searchTime, startTime): #Calculates the position that the player would be at searchTime. Returns a pos if the player lives or a time if the player dies
        currentPos = Vector2(0, 0)
        currentTile = None
        
        tile = level.getTileAt(currentPos, startTime)
        if tile is None:
            #print("dead1")
            return startTime #If there's no tile at the start then you die at the start
        #print("live1")
        currentTile = tile #Otherwise that's the tile you're on

        for move in self.moves:
            moveTime = move[1]
            
            if moveTime > searchTime:
                return currentPos #If you've reached the time you want to, then you are alive and at your current pos
            
            tile = level.getTileAt(currentPos, moveTime)
            if tile != currentTile:
                #print("dead2")
                return currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
            #print("live2")
            
            currentPos += move[0] #Make the move you were trying to make
            tile = level.getTileAt(currentPos, moveTime)
            if tile is None:
                #print("dead3")
                return moveTime #If you move to nothing then you die at the time of your move
            #print("live3")
            currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(currentPos, searchTime) #If your last move was made before the search time
        if tile != currentTile:
            #print("dead4", tile.pos, currentTile.pos)
            return currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
        #print("live4")
        return currentPos
    
    def calculateVisiblePos(self, level, searchTime, startTime):
        currentPos = self.calculatePos(level, searchTime, startTime)
        
        if len(self.moves) > 1:
            lastMoveTime = self.moves[-1][1]
            lastMovePos = self.calculatePos(level, self.moves[-2][1], startTime)
        elif len(self.moves) == 1:
            lastMoveTime = self.moves[0][1]
            lastMovePos = Vector2(0, 0)
        else:
            lastMoveTime = 0
            lastMovePos = Vector2(0, 0)
        
        print(currentPos, lastMovePos, searchTime, lastMoveTime)
        
        x = easeOutPow(lastMovePos.x, currentPos.x, lastMoveTime, lastMoveTime + self.moveTime, 1, min(searchTime, lastMoveTime + self.moveTime))
        y = easeOutPow(lastMovePos.y, currentPos.y, lastMoveTime, lastMoveTime + self.moveTime, 1, min(searchTime, lastMoveTime + self.moveTime))
        return Vector2(x, y)