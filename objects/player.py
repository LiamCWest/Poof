from images import images
import pygame
import bisect
from utils.vector2 import Vector2
from utils.binarySearch import binarySearch
from graphics.animation import *
from utils.resizingFuncs import blitResized
from logic.song.timingPoints import getNextBeat, getPreviousBeat, getNearestBeat

class PlayerState:
    def __init__(self):
        self.time = None
        self.pos = None
        self.visiblePos = None
        self.direction = None #a vector2
        self.animState = None #standing, walking, gliding, dead
        self.acc = None
        self.deathTime = None
        self.gliding = False
        self.glideStartPos = None
        self.glideDir = None

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
        
        blitResized(win, img, self.offset, size, self.factor)
        #win.blit(pygame.transform.scale(img, size.toTuple()), (size * self.offset).toTuple())
        
    def move(self, diff, time):
        self.moves.append((diff, time, True))
        
    def stopMove(self, diff, time):
        self.moves.append((diff, time, False))

    def calculateState(self, level, searchTime):
        if searchTime < self.startTime:
            return None #cant have a state if the player isnt in the level yet
        
        def calculateAcc(currentAcc, movesMade, tileTime, time):
            thisAcc = abs(tileTime - time)
            return (currentAcc * (movesMade - 1) + thisAcc) / movesMade #weighted average           
        
        state = PlayerState()
        state.time = searchTime
        state.countedMovesMade = 0
        state.acc = 0
        
        state.pos = self.startPos.copy()
        state.visiblePos = self.startPos.copy()
        currentTile = None
        
        state.direction = Vector2(0, 1)
        state.animState = "standing"
        
        tile = level.getTileAt(state.pos, self.startTime)
        if tile is None:
            state.deathTime = self.startTime
            state.animState = "dead"
            return #If there's no tile at the start then you die at the start
        currentTile = tile #Otherwise that's the tile you're on

        for i, move in enumerate(self.moves):
            moveTime = move[1]
            if moveTime > searchTime:
                return state #If you've reached the time you want to, then you are alive and at your current pos
            
            if not move[2]: #if your last move is a key release
                if state.gliding and state.glideDir == move[0]: #if you release the glide while you're gliding, that means you must be over the void and die
                    state.deathTime = move[1]
                    state.animState = "dead"
                    return state
                else: #else dont care about releases
                    continue
                
            state.direction = move[0]
            
            #the move must now be a press
            tile = level.getTileAt(state.pos, moveTime)
            if tile != currentTile:
                state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
                state.animState = "dead"
                return state
            
            if tile is not None and tile.type == "glide": #if you move off a glide tile
                state.gliding = True
                state.glideStartPos = tile.pos
                state.glideDir = move[0]

                nextPressTime = float("inf")
                j = i + 1
                while j < len(self.moves):
                    if self.moves[j][2]:
                        nextPressTime = self.moves[j][1] #get the time of the next press move
                        break
                    j += 1
                glideEndTime = min(state.time, nextPressTime) #calculate the glide until that time
                glideTimeOffset = move[1] - tile.disappearTime #the time off of the perfect glide time that you're gliding
                
                glidePositions = []
                glidePositions.append(move[1])
                
                timeInRange = getPreviousBeat(level.timingPoints, tile.disappearTime, tile.divisor * 2)
                while True:
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2)
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2)
                    glidePositions.append(timeInRange + glideTimeOffset)
                    if timeInRange + glideTimeOffset > glideEndTime:
                        break
                
                isTileHit = False
                for i, glide in enumerate(glidePositions[:-1]): #check if you hit a tile while you were gliding
                    pos = state.glideStartPos + move[0].multiply(i)
                    tilesHit = level.getTilesOverlapping(pos, glide, glidePositions[i + 1])
                    for tile2 in tilesHit:
                        if tile2 == tile:
                            continue
                        timeHit = max(tile2.appearedTime - level.appearLength, glide)
                        if timeHit > state.time:
                            continue
                        
                        tileHit = tile2
                        state.pos = tileHit.pos
                        
                        lastMoveIndex = i
                        nextMoveIndex = i + 1
                        timeInLastRange = glidePositions[lastMoveIndex]
                        timeInNextRange = glidePositions[nextMoveIndex]
                        lastDistance = lastMoveIndex - 0.5
                        nextDistance = nextMoveIndex - 0.5
                        state.visiblePos = state.glideStartPos + move[0].multiply(min(lastMoveIndex, lerp(lastDistance, nextDistance, timeInLastRange, timeInNextRange, state.time), lastMoveIndex))
                        
                        if state.time > timeInNextRange:
                            state.animState = "standing"
                        else:
                            state.animState = "gliding"
                        
                        state.gliding = False #and you're on a tile so you're not gliding anymore
                        state.glideStartPos = None
                        state.glideDir = None
                        currentTile = tileHit
                        isTileHit = True
                        break
                    else:
                        continue
                    break
                    
                if isTileHit:
                    continue
                
                #else you're still gliding                        
                lastMoveIndex = bisect.bisect_right(glidePositions, glideEndTime) - 1
                nextMoveIndex = lastMoveIndex + 1
                state.pos = state.glideStartPos + move[0].multiply(lastMoveIndex) #pos goes to glide pos
                
                timeInLastRange = glidePositions[lastMoveIndex]
                timeInNextRange = glidePositions[nextMoveIndex]
                lastDistance = max(lastMoveIndex - 0.5, 0)
                nextDistance = nextMoveIndex - 0.5
                state.visiblePos = state.glideStartPos + move[0].multiply(lerp(lastDistance, nextDistance, timeInLastRange, timeInNextRange, glideEndTime))
                
                state.animState = "gliding"
                
                currentTile = None #you're not on a tile cause you're gliding
                
            else: #else move normally
                state.gliding = False
                state.glideStartPos = None
                state.glideDir = None
                state.pos += move[0] #Make the move you were trying to make

                lastPos = state.pos - move[0]
                lastTime = move[1]
                thisPos = state.pos
                thisTime = move[1] + self.moveLength
                x = easeOutPow(lastPos.x, thisPos.x, lastTime, thisTime, 3, state.time)
                y = easeOutPow(lastPos.y, thisPos.y, lastTime, thisTime, 3, state.time)
                state.visiblePos = Vector2(x, y)
                
                if state.time > lastTime:
                    state.animState = "standing"
                else:
                    state.animState = "walking"
                
                tile = level.getTileAt(state.pos, moveTime)
                if tile is None:
                    state.deathTime = moveTime #If you move to nothing then you die at the time of your move
                    state.animState = "dead"
                    return state
                
                currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(state.pos, searchTime) #If your last move was made before the search time
        if tile != currentTile and not state.gliding:
            state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before, then you died
            state.animState = "dead"
            return state
        return state