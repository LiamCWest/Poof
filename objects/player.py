from images import images
import pygame
from utils.vector2 import Vector2
from utils.binarySearch import binarySearch
from graphics.animation import *

class PlayerState:
    def __init__(self):
        self.time = None
        self.pos = None
        self.visiblePos = None
        self.lastMove = None
        self.countedMovesMade = None
        self.averageAcc = None
        self.deathTime = None

class Player:
    offset = Vector2(5, 4)
    moveLength = 0.2
    def __init__(self, startPos, startTime):
        self.startPos = startPos
        self.startTime = startTime
                
        self.moves = [] #Tuple of (diff, time)
        self.deathTime = None
        
    def draw(self, win, state): 
        if state is None:
            return
        
        size = Vector2(50, 50)
        
        pos = state.pos
        visiblePos = state.visiblePos
        time = state.time
        
        if len(self.moves) == 0:
            img = images.images["player_down"]
        else:
            lastMove = self.moves[binarySearch(self.moves, time, lambda x, y: x - y[1])][0]
            if pos != visiblePos: #moving
                if lastMove == Vector2(-1, 0):
                    img = images.images["player_left_moving"]
                elif lastMove == Vector2(0, -1):
                    img = images.images["player_up_moving"]
                elif lastMove == Vector2(1, 0):
                    img = images.images["player_right_moving"]
                else:
                    img = images.images["player_down_moving"]
            else:
                if lastMove == Vector2(-1, 0):
                    img = images.images["player_left"]
                elif lastMove == Vector2(0, -1):
                    img = images.images["player_up"]
                elif lastMove == Vector2(1, 0):
                    img = images.images["player_right"]
                else:
                    img = images.images["player_down"]
        
        win.blit(pygame.transform.scale(img, size.toTuple()), (size * self.offset).toTuple())
        
    def move(self, diff, time):
        self.moves.append((diff, time))
        
    def die(self, time):
        self.deathTime = time
        
    def calculatePos(self, level, searchTime): #Calculates the position that the player would be at searchTime. Returns a pos if the player lives or a (pos, time) if the player dies
        if searchTime < self.startTime:
            return None
        
        currentPos = self.startPos.copy()
        currentTile = None
        
        tile = level.getTileAt(currentPos, self.startTime)
        if tile is None:
            return currentPos, self.startTime #If there's no tile at the start then you die at the start
        currentTile = tile #Otherwise that's the tile you're on

        for move in self.moves:
            moveTime = move[1]
            
            if moveTime > searchTime:
                return currentPos #If you've reached the time you want to, then you are alive and at your current pos
            
            tile = level.getTileAt(currentPos, moveTime)
            if tile != currentTile:
                return currentPos, currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
            
            currentPos += move[0] #Make the move you were trying to make
            tile = level.getTileAt(currentPos, moveTime)
            if tile is None:
                return currentPos, moveTime #If you move to nothing then you die at the time of your move
            currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(currentPos, searchTime) #If your last move was made before the search time
        if tile != currentTile:
            return currentPos, currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
        return currentPos
    
    def calculateVisiblePos(self, level, searchTime): #Calculates the visible position of the player at searchTime
        if searchTime < self.startTime:
            return None
        
        currentPos = self.calculatePos(level, searchTime)
        if isinstance(currentPos, tuple):
            currentPos = currentPos[0]
        
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
            if isinstance(lastMovePos, tuple):
                lastMovePos = lastMovePos[0]
        
        x = easeOutPow(lastMovePos.x, currentPos.x, lastMoveTime, lastMoveTime + self.moveLength, 3.5, min(searchTime, lastMoveTime + self.moveLength))
        y = easeOutPow(lastMovePos.y, currentPos.y, lastMoveTime, lastMoveTime + self.moveLength, 3.5, min(searchTime, lastMoveTime + self.moveLength))
        return Vector2(x, y)
    
    def calculateState(self, level, searchTime):
        if searchTime < self.startTime:
            return None #cant have a state if the player isnt in the level yet
        
        def calculatePosMovesDeathTime(state):
            state.countedMovesMade = 0
            
            state.pos = self.startPos.copy()
            currentTile = None
            
            tile = level.getTileAt(state.pos, self.startTime)
            if tile is None:
                state.deathTime =self.startTime
                return #If there's no tile at the start then you die at the start
            currentTile = tile #Otherwise that's the tile you're on

            for move in self.moves:
                moveTime = move[1]
                
                if moveTime > searchTime:
                    return #If you've reached the time you want to, then you are alive and at your current pos
                
                state.lastMove = move
                state.countedMovesMade += 1
                
                tile = level.getTileAt(state.pos, moveTime)
                if tile != currentTile:
                    state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
                    return
                
                state.pos += move[0] #Make the move you were trying to make
                tile = level.getTileAt(state.pos, moveTime)
                if tile is None:
                    state.deathTime = moveTime #If you move to nothing then you die at the time of your move
                    return
                currentTile = tile #Otherwise that's the tile you're on
                
            tile = level.getTileAt(state.pos, searchTime) #If your last move was made before the search time
            if tile != currentTile:
                state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
                return
        
        def addVisiblePos(state):
            time = state.deathTime if state.deathTime is not None else state.time
            lastMovePos = state.pos - state.lastMove[0] if state.lastMove is not None else Vector2(0, 0)
            lastMoveTime = state.lastMove[1] if state.lastMove is not None else self.startTime
            x = easeOutPow(lastMovePos.x, state.pos.x, lastMoveTime, lastMoveTime + self.moveLength, 3.5, min(time, lastMoveTime + self.moveLength))
            y = easeOutPow(lastMovePos.y, state.pos.y, lastMoveTime, lastMoveTime + self.moveLength, 3.5, min(time, lastMoveTime + self.moveLength))
            state.visiblePos = Vector2(x, y)
        
        state = PlayerState()
        state.time = searchTime
        calculatePosMovesDeathTime(state)
        addVisiblePos(state)
        return state