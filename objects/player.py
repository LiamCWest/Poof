from images import images
import pygame
import bisect
from utils.vector2 import Vector2
from utils.binarySearch import binarySearch
from graphics.animation import *
from logic.song.timingPoints import getNextBeat, getPreviousBeat, getNearestBeat

class PlayerState:
    def __init__(self):
        self.time = None
        self.pos = None
        self.visiblePos = None
        self.direction = None #a vector2
        self.animState = None #standing, walking, gliding, dead
        self.acc = None
        self.offset = None
        self.movesMade = None
        self.accMovesMade = None
        self.deathTime = None

class Player:
    offset = Vector2(5.9, 3.1) #TODO: Don't hardcode these values
    moveLength = 0.2
    def __init__(self, startPos, startTime):
        self.startPos = startPos
        self.startTime = startTime
                
        self.moves = [] #Tuple of (diff, time, isPress)
        
    def draw(self, win, state): 
        if state is None:
            return
        
        size = 100
        
        if state.animState in ["walking", "gliding"]: #moving
            imgs = {
                Vector2(-1, 0): images.images["player_left_moving"],
                Vector2(0, -1): images.images["player_up_moving"],
                Vector2(1, 0): images.images["player_right_moving"],
                Vector2(0, 1): images.images["player_down_moving"]
            }
        else:
            imgs = {
                Vector2(-1, 0): images.images["player_left"],
                Vector2(0, -1): images.images["player_up"],
                Vector2(1, 0): images.images["player_right"],
                Vector2(0, 1): images.images["player_down"]
            }
        img = imgs[state.direction]
        
        if state.deathTime is not None:
            deadScale = easeInPow(1, 0, state.deathTime, state.deathTime + 0.3, 2, state.time)
        else:
            deadScale = 1
        win.blit(pygame.transform.scale(img, (size * deadScale, size * deadScale)), self.offset.add((1 - deadScale) / 2).multiply(size).toTuple())
        
    def move(self, diff, time):
        self.moves.append((diff, time, True))
        
    def stopMove(self, diff, time):
        self.moves.append((diff, time, False))

    def calculateState(self, level, searchTime):
        if searchTime < self.startTime:
            return None #cant have a state if the player isnt in the level yet
        
        def calculateAcc(currentAcc, movesMade, tileTime, time):
            thisAcc = abs(time - tileTime)
            return (currentAcc * (movesMade - 1) + thisAcc) / movesMade #weighted average
        
        def calculateOffset(currentOffset, movesMade, tileTime, time):
            thisOffset = time - tileTime
            return (currentOffset * (movesMade - 1) + thisOffset) / movesMade #another weighted average
        
        state = PlayerState() #create an empty state
        state.time = searchTime #this is the time of the state, obviously
        state.acc = 0
        state.offset = 0
        state.movesMade = 0
        state.accMovesMade = 0
        
        state.pos = self.startPos.copy() #state pos starts at the player's start pos
        state.visiblePos = self.startPos.copy() #same with visual pos
        
        state.direction = Vector2(0, 1) #default values
        state.animState = "standing"
        
        currentTile = None #values that are kinda player state but not important enough to actually be in state
        gliding = False
        glideStartPos = None
        glideDir = None
        
        tile = level.getTileAt(state.pos, self.startTime)
        if tile is None:
            state.deathTime = self.startTime
            state.animState = "dead"
            return #If there's no tile at the start then you die at the start
        currentTile = tile #Otherwise that's the tile you're on

        for i, move in enumerate(self.moves): #run through all the moves
            moveTime = move[1]
            if moveTime > searchTime:
                return state #If you've reached the time you want to, then you are alive and at your current pos
            
            if not move[2]: # if the move is a key release
                if gliding and glideDir == move[0]: #if you release the glide while you're gliding, that means you must be over the void and die
                    state.deathTime = move[1]
                    state.animState = "dead"
                    return state
                else: #else dont care about releases
                    continue
                
            state.direction = move[0] #the direction you're moving is the direction you're moving, obviously
            
            #the move must now be a press
            tile = level.getTileAt(state.pos, moveTime) #get the tile that you moved off of
            if tile != currentTile:
                state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
                state.animState = "dead"
                return state
            
            if tile is not None and tile.type == "glide": #if you move off a glide tile
                gliding = True #all of the stuff that's obviously happening cause you're gliding
                glideStartPos = tile.pos
                glideDir = move[0]

                nextPressTime = float("inf")
                if i + 1 < len(self.moves):
                    nextPressTime = self.moves[i + 1][1] #get the time of the next press move
                glideEndTime = min(state.time, nextPressTime) #wanna calculate the glide until the glide should end
                glideTimeOffset = move[1] - tile.disappearTime #the time off of the "perfect" glide time that you're gliding
                
                timeAtGlideDistances = [] #an array of all the times you will be various distances away from the glide start pos
                timeAtGlideDistances.append(move[1]) #you are at your current pos at your current time, obviously
                
                timeInRange = getPreviousBeat(level.timingPoints, tile.disappearTime, tile.divisor * 2) #get half a beat offset, because you actually move on offbeats
                while True:
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2)
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2) #go one beat forward
                    timeAtGlideDistances.append(timeInRange + glideTimeOffset) #add your new time
                    if timeInRange + glideTimeOffset > glideEndTime: #if you've glided past the end time, then no need to care about what happens later
                        break
                
                isTileHit = False
                for i, glide in enumerate(timeAtGlideDistances[:-1]): #loop over all the positions you would be at while gliding
                    pos = glideStartPos + move[0].multiply(i) #get the position
                    tilesHit = level.getTilesOverlapping(pos, glide, timeAtGlideDistances[i + 1]) #check if there were any tiles while you were on that position
                    for tile2 in tilesHit: #loop over all the tiles
                        if tile2 == tile: #if its the tile you start on, dont care
                            continue
                        timeHit = max(tile2.appearedTime - level.appearLength, glide)
                        if timeHit > state.time: #if its after the current time, dont care
                            continue
                        
                        state.pos = tile2.pos #the position you're at after landing on the tile
                        
                        #do some stupid interpolation to get the visible pos, because it lags behind the actual pos for reasons
                        lastMoveIndex = i
                        nextMoveIndex = i + 1
                        timeAtLastPos = timeAtGlideDistances[lastMoveIndex]
                        timeAtNextPos = timeAtGlideDistances[nextMoveIndex]
                        lastDistance = lastMoveIndex - 0.5
                        nextDistance = nextMoveIndex - 0.5
                        state.visiblePos = glideStartPos + move[0].multiply(min(lastMoveIndex, lerp(lastDistance, nextDistance, timeAtLastPos, timeAtNextPos, state.time), lastMoveIndex))
                        
                        state.movesMade += 1
                        if tile.type != "rest":
                            state.accMovesMade += 1
                            state.acc = calculateAcc(state.acc, state.accMovesMade, tile2.appearedTime, timeHit) #update acc and offset
                            state.offset = calculateOffset(state.offset, state.accMovesMade, tile2.appearedTime, timeHit)
                        
                        #if you've passed the time where you have visibly landed on the tile, you're standing. else, you're gliding
                        if state.time > timeAtNextPos:
                            state.animState = "standing"
                        else:
                            state.animState = "gliding"
                        
                        gliding = False #and you're on a tile so you're not gliding anymore
                        glideStartPos = None
                        glideDir = None
                        currentTile = tile2 #and you're on a tile
                        isTileHit = True
                        break #stupid mess to break out of these 2 loops and then continue the 3rd loop cause python doesn't have labeled breaks
                    else:
                        continue
                    break
                    
                if isTileHit:
                    continue
                
                #else you're still gliding                        
                lastMoveIndex = len(timeAtGlideDistances) - 2 #because of how timeAtGlideDistances works, the 2nd last entry is always the index of the last move
                nextMoveIndex = lastMoveIndex + 1
                state.pos = glideStartPos + move[0].multiply(lastMoveIndex) #pos goes to glide pos
                
                #more lerp stuff
                timeAtLastPos = timeAtGlideDistances[lastMoveIndex]
                timeAtNextPos = timeAtGlideDistances[nextMoveIndex]
                lastDistance = max(lastMoveIndex - 0.5, 0)
                nextDistance = nextMoveIndex - 0.5
                state.visiblePos = glideStartPos + move[0].multiply(lerp(lastDistance, nextDistance, timeAtLastPos, timeAtNextPos, glideEndTime))
                
                state.animState = "gliding"
                
                currentTile = None #you're not on a tile cause you're gliding
                
            else: #else move normally
                gliding = False
                glideStartPos = None
                glideDir = None
                state.pos += move[0] #Make the move you were trying to make

                #morier interp stuff
                lastPos = state.pos - move[0]
                lastTime = move[1]
                thisPos = state.pos
                thisTime = move[1] + self.moveLength
                x = easeOutPow(lastPos.x, thisPos.x, lastTime, thisTime, 3, state.time)
                y = easeOutPow(lastPos.y, thisPos.y, lastTime, thisTime, 3, state.time)
                state.visiblePos = Vector2(x, y)
                
                
                #if you've passed the time when the interp ends, you're standing. otherwise, you're walking
                if state.time > thisTime:
                    state.animState = "standing"
                else:
                    state.animState = "walking"
                
                tile = level.getTileAt(state.pos, moveTime)
                if tile is None:
                    state.deathTime = moveTime #If you move to nothing then you die at the time of your move
                    state.animState = "dead"
                    return state
                
                state.movesMade += 1
                if tile.type != "rest":
                    state.accMovesMade += 1
                    state.acc = calculateAcc(state.acc, state.accMovesMade, tile.appearedTime, move[1])
                    state.offset = calculateOffset(state.offset, state.accMovesMade, tile.appearedTime, move[1])
                
                currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(state.pos, searchTime) #If your last move was made before the search time
        if tile != currentTile and not gliding:
            state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
            state.animState = "dead"
            return state
        
        return state