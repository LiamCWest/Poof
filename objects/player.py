from images import images
import pygame
from utils.vector2 import Vector2
from utils.binarySearch import binarySearch
from graphics.animation import *

class Player:
    offset = Vector2(5, 4)
    moveTime = 0.1
    def __init__(self, startPos, startTime):
        self.startPos = startPos
        self.startTime = startTime
                
        self.moves = [] #Tuple of (diff, time)
        
    def draw(self, win):
        size = Vector2(50, 50)
        img = images.images["player"]
        
        win.blit(pygame.transform.scale(img, size.toTuple()), (size * self.offset).toTuple())
        
    def move(self, diff, time):
        self.moves.append((diff, time))
        
    def calculatePos(self, level, searchTime): #Calculates the position that the player would be at searchTime. Returns a pos if the player lives or a time if the player dies
        if searchTime < self.startTime:
            return None
        
        currentPos = self.startPos.copy()
        currentTile = None
        
        tile = level.getTileAt(currentPos, self.startTime)
        if tile is None:
            return self.startTime #If there's no tile at the start then you die at the start
        currentTile = tile #Otherwise that's the tile you're on

        for move in self.moves:
            moveTime = move[1]
            
            if moveTime > searchTime:
                return currentPos #If you've reached the time you want to, then you are alive and at your current pos
            
            tile = level.getTileAt(currentPos, moveTime)
            if tile != currentTile:
                return currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
            
            currentPos += move[0] #Make the move you were trying to make
            tile = level.getTileAt(currentPos, moveTime)
            if tile is None:
                return moveTime #If you move to nothing then you die at the time of your move
            currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(currentPos, searchTime) #If your last move was made before the search time
        if tile != currentTile:
            return currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
        return currentPos
    
    def calculateVisiblePos(self, level, searchTime): #Calculates the visible position of the player at searchTime
        if searchTime < self.startTime:
            return None
        
        currentPos = self.calculatePos(level, searchTime)
        
        moveJustMadeIndex = binarySearch(self.moves, searchTime, lambda x, y: x - y[1])
        if moveJustMadeIndex is None or moveJustMadeIndex < 0:
            lastMoveTime = 0
            lastMovePos = self.startPos
        elif moveJustMadeIndex == 0:
            lastMoveTime = self.moves[moveJustMadeIndex][1]
            lastMovePos = self.startPos
        elif moveJustMadeIndex > 0:
            lastMoveTime = self.moves[moveJustMadeIndex][1]
            lastMovePos = self.calculatePos(level, self.moves[moveJustMadeIndex - 1][1])
        
        x = easeOutPow(lastMovePos.x, currentPos.x, lastMoveTime, lastMoveTime + self.moveTime, 2, min(searchTime, lastMoveTime + self.moveTime))
        y = easeOutPow(lastMovePos.y, currentPos.y, lastMoveTime, lastMoveTime + self.moveTime, 2, min(searchTime, lastMoveTime + self.moveTime))
        return Vector2(x, y)