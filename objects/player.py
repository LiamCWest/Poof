# external imports
import pygame #pygame

# internal imports
from images import images #for images
from utils.vector2 import Vector2 #for Vector2
from utils.binarySearch import binarySearch #for binarySearch
from graphics.animation import * #for anim features
from logic.song.timingPoints import getNextBeat, getPreviousBeat, getNearestBeat #for timing point features

class PlayerState: #a struct representing the state of a player at a specific time
    def __init__(self): #init to default
        self.time = None #the time of the state
        self.pos = None #the position of the player in this state
        self.visiblePos = None #the visible position of the player in this state
        self.direction = None #a vector2
        self.animState = None #standing, walking, gliding, dead
        self.acc = None #the player's current accuracy
        self.offset = None #the player's current offset
        self.movesMade = None #the number of moves the player has made
        self.accMovesMade = None #the number of moves the player has made that affect accuracy
        self.deathTime = None #the time the player has died, if they have died

class Player: #a class representing a player
    offset = Vector2(5.9, 3.1) #the player's offset in tiles required for it to be centered on the screen
    moveLength = 0.2 #the time it takes for the player to move 1 tile
    deathLength = 0.3 #the time it takes for the player's death anim
    def __init__(self, startPos, startTime): #init to default
        self.startPos = startPos #sets the startPos
        self.startTime = startTime #sets the start time
                
        self.moves = [] #Tuple of (diff, time, isPress)
        
    def draw(self, win, state): #draws the player to a window based on its state
        if state is None: #if there is no state, there is no player
            return #so return
        
        size = 100 #set the size of the player in pixels
        
        if state.animState in ["walking", "gliding"]: #moving
            imgs = { #a dictionary of images for each direction
                Vector2(-1, 0): images.images["player_left_moving"], #left
                Vector2(0, -1): images.images["player_up_moving"], #up 
                Vector2(1, 0): images.images["player_right_moving"], #right
                Vector2(0, 1): images.images["player_down_moving"] #down
            }
        else: #not moving
            imgs = { #a dictionary of images for each direction
                Vector2(-1, 0): images.images["player_left"], #left
                Vector2(0, -1): images.images["player_up"], #up
                Vector2(1, 0): images.images["player_right"], #right
                Vector2(0, 1): images.images["player_down"] #down
            }
        img = imgs[state.direction] #set the image used to the correct one
        
        if state.deathTime is not None: #if you're dead
            deadScale = easeInPow(1, 0, state.deathTime, state.deathTime + self.deathLength, 2, state.time) #calculate the size of the player in its death animation
        else: #if you're not
            deadScale = 1 #death anim isn't playing so you're at full size
        win.blit(pygame.transform.scale(img, (size * deadScale, size * deadScale)), self.offset.add((1 - deadScale) / 2).multiply(size).toTuple()) #draw the player to the center of the screen
        
    def move(self, diff, time): #adds a "press" move to the player
        self.moves.append((diff, time, True)) #append move tuple
        
    def stopMove(self, diff, time): #adds a "release" move to the player
        self.moves.append((diff, time, False)) #append move tuple

    def calculateState(self, level, searchTime): #calculates the state of the player at a certain time
        if searchTime < self.startTime: #if the search time is before the player starts, return None
            return None #cant have a state if the player isnt in the level yet
        
        def calculateAcc(currentAcc, movesMade, tileTime, time): #calculates the new accuracy of the player after a move
            thisAcc = abs(time - tileTime) #the accuracy of this move
            return (currentAcc * (movesMade - 1) + thisAcc) / movesMade #weighted average
        
        def calculateOffset(currentOffset, movesMade, tileTime, time): #calculates the new offset of the player after a move
            thisOffset = time - tileTime #the offset of this move
            return (currentOffset * (movesMade - 1) + thisOffset) / movesMade #another weighted average
        
        state = PlayerState() #create an empty state
        state.time = searchTime #this is the time of the state, obviously
        state.acc = 0 #your acc is 0 at the start
        state.offset = 0 #your offset is 0 at the start
        state.movesMade = 0 #you have made 0 moves at the start
        state.accMovesMade = 0 #you have made 0 acc affecting moves at the start
        
        state.pos = self.startPos.copy() #state pos starts at the player's start pos
        state.visiblePos = self.startPos.copy() #same with visual pos
        
        state.direction = Vector2(0, 1) #you are facing down at the start
        state.animState = "standing" #you are standing at the start
        
        currentTile = None #values that are kinda player state but not important enough to actually be in state
        gliding = False #you're not gliding at the start
        glideStartPos = None #you're not gliding at the start
        glideDir = None #you're not gliding at the start
        
        tile = level.getTileAt(state.pos, self.startTime) #get the tile that you start on
        if tile is None: #if there's no tile at the start
            state.deathTime = self.startTime #you die at the start
            state.animState = "dead" #you're dead at the start
            return state #so return the dead state
        currentTile = tile #Otherwise that's the tile you're on

        for i, move in enumerate(self.moves): #run through all the moves
            if move[1] > searchTime: #if the move is after the search time
                return state #If you've reached the time you want to, then you are alive and at your current pos
            
            if not move[2]: # if the move is a key release
                if gliding and glideDir == move[0]: #if you release the glide while you're gliding, that means you must be over the void and die
                    state.deathTime = move[1] #you die at the time of the release
                    state.animState = "dead" #you're dead at the time of the release
                    return state #so return the dead state
                else: #else dont care about releases
                    continue #so continue to the next move
            
            #the move must now be a press
            state.direction = move[0] #the direction you're moving is the direction you're moving, obviously
            
            tile = level.getTileAt(state.pos, move[1]) #get the tile that you moved off of
            if tile != currentTile and currentTile is not None: #if you moved off of a tile and you were on a tile before
                state.deathTime = currentTile.disappearTime + level.disappearLength #If you're not on the same tile as before when you start moving, then you died
                state.animState = "dead" #you're dead at the time of the move
                return state #so return the dead state
            
            if tile is not None and tile.type == "glide": #if you move off a glide tile
                gliding = True #all of the stuff that's obviously happening cause you're gliding
                glideStartPos = tile.pos #you start gliding at the tile you moved off of
                glideDir = move[0] #you're gliding in the direction you moved

                nextImportantMoveTime = float("inf") #the time of the next move that will affect your glide
                j = i + 1 #start at the next move
                while j < len(self.moves): #loop through all the moves after this one
                    testedMove = self.moves[j] #get the move
                    if testedMove[0] == move[0] and not testedMove[2]: #glide should end when you release the dash direction
                        nextImportantMoveTime = testedMove[1] #get the time of the next release move
                        break #break out of the loop
                    if testedMove[2]: #or when you press another key
                        nextImportantMoveTime = testedMove[1] #get the time of the next press move
                        break #break out of the loop
                    j += 1 #increment j
                glideEndTime = min(state.time, nextImportantMoveTime) #wanna calculate the glide until the glide should end
                glideTimeOffset = move[1] - tile.disappearTime #the time off of the "perfect" glide time that you're gliding
                
                timeAtGlideDistances = [] #an array of all the times you will be various distances away from the glide start pos
                timeAtGlideDistances.append(move[1]) #you are at your current pos at your current time, obviously
                
                timeInRange = getPreviousBeat(level.timingPoints, tile.disappearTime, tile.divisor * 2) #get half a beat offset, because you actually move on offbeats
                while True: #loop until you've passed the glide end time
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2) #go half a beat forward
                    timeInRange = getNextBeat(level.timingPoints, timeInRange, tile.divisor * 2) #go one beat forward in total
                    timeAtGlideDistances.append(timeInRange + glideTimeOffset) #add your new time
                    if timeInRange + glideTimeOffset > glideEndTime: #if you've glided past the end time, then no need to care about what happens later
                        break #so break out of the loop
                
                isTileHit = False #you haven't hit a tile yet
                for i, glide in enumerate(timeAtGlideDistances[:-1]): #loop over all the positions you would be at while gliding
                    pos = glideStartPos + move[0].multiply(i) #get the pos you would be at
                    
                    tileHitTimeCheck = glide #start checking at the time you would be at that pos
                    while tileHitTimeCheck < timeAtGlideDistances[i + 1] and tileHitTimeCheck < state.time: #while you're not past the time you would be at the next pos and you're not past the time you're looking for
                        tileAtTime = level.getTileAt(pos, tileHitTimeCheck) #get the tile you're on at that time
                        if tileAtTime is None: #if you're not on any tile, die
                            state.deathTime = tileHitTimeCheck #you die at the time you're not on a tile
                            state.animState = "dead" #you're dead
                            state.pos = pos #you're at the pos you would be at
                            lastMoveIndex = i #the last glide that happened
                            nextMoveIndex = i + 1 #the next glide that would happen if you didn't die
                            timeAtLastPos = timeAtGlideDistances[lastMoveIndex] #the tiem you were at that pos 
                            timeAtNextPos = timeAtGlideDistances[nextMoveIndex] #the time you would be at the next pos
                            lastDistance = lastMoveIndex - 0.5 #your real position (for interpolation purposes)
                            nextDistance = nextMoveIndex - 0.5 #the next real position (for interpolation purposes)
                            state.visiblePos = glideStartPos + move[0].multiply(min(lastMoveIndex, lerp(lastDistance, nextDistance, timeAtLastPos, timeAtNextPos, state.time))) #lerp between last and next pos
                            return state #return the dead state
                        if tileAtTime == tile: #if its the tile you start on, dont care
                            tileHitTimeCheck = math.nextafter(tileAtTime.disappearTime + level.disappearLength, float("inf")) #check the time after this tile is gone
                            continue #and continue
                        if tileAtTime.type == "glidePath": #glide paths are ignored
                            tileHitTimeCheck = math.nextafter(tileAtTime.disappearTime + level.disappearLength, float("inf")) #check the time after this tile is gone
                            continue #and continue
                        state.pos = tileAtTime.pos #else you're at the pos of the tile you hit
                        
                        #do some stupid interpolation to get the visible pos, because it lags behind the actual pos for reasons
                        lastMoveIndex = i #the last glide that happened
                        nextMoveIndex = i + 1 #the next glide that would happen if you didn't die
                        timeAtLastPos = timeAtGlideDistances[lastMoveIndex] #the tiem you were at that pos 
                        timeAtNextPos = timeAtGlideDistances[nextMoveIndex] #the time you would be at the next pos
                        lastDistance = lastMoveIndex - 0.5 #your real position (for interpolation purposes)
                        nextDistance = nextMoveIndex - 0.5 #the next real position (for interpolation purposes)
                        state.visiblePos = glideStartPos + move[0].multiply(min(lastMoveIndex, lerp(lastDistance, nextDistance, timeAtLastPos, timeAtNextPos, state.time))) #lerp between last and next pos
                        
                        state.movesMade += 1 #you've made a move
                        if tile.type != "rest": #if you're not on a rest tile
                            state.accMovesMade += 1 #you've made a move that counts towards acc
                            state.acc = calculateAcc(state.acc, state.accMovesMade, tileAtTime.appearedTime, tileHitTimeCheck) #update acc
                            state.offset = calculateOffset(state.offset, state.accMovesMade, tileAtTime.appearedTime, tileHitTimeCheck) #update offset
                        
                        if state.time > timeAtNextPos: #if you've passed the time when the interp ends
                            state.animState = "standing" #you're standing
                        else: #otherwise
                            state.animState = "gliding" #you're gliding
                        
                        gliding = False #and you're on a tile so you're not gliding anymore
                        glideStartPos = None #you're not gliding
                        glideDir = None #you're not gliding
                        currentTile = tileAtTime #and you're on a tile
                        isTileHit = True #you hit a tile
                        break #stupid mess to break out of these 2 loops and then continue the 3rd loop cause python doesn't have labeled breaks
                    else: #if you didn't break
                        continue #continue the outer loop
                    break #otherwise break the outer loop
                    
                if isTileHit: #if you hit a tile
                    continue #continue to the next move
                
                #else you're still gliding                        
                lastMoveIndex = len(timeAtGlideDistances) - 2 #because of how timeAtGlideDistances works, the 2nd last entry is always the index of the last move
                nextMoveIndex = lastMoveIndex + 1 #and ditto for the next move
                state.pos = glideStartPos + move[0].multiply(lastMoveIndex) #pos goes to glide pos
                
                #more lerp stuff
                timeAtLastPos = timeAtGlideDistances[lastMoveIndex] #the time you were at the last distance
                timeAtNextPos = timeAtGlideDistances[nextMoveIndex] #the time you would have been at the next distance
                lastDistance = max(lastMoveIndex - 0.5, 0) #the real distance you were from the tile before dying (for interpolation), cant be negative
                nextDistance = nextMoveIndex - 0.5 #the real distance you would have been from the tile after dying (for interpolation)
                state.visiblePos = glideStartPos + move[0].multiply(lerp(lastDistance, nextDistance, timeAtLastPos, timeAtNextPos, glideEndTime)) #lerp between the last pos and the next pos
                
                currentTile = None #you're not on a tile cause you're gliding
                
                state.animState = "gliding" #you're gliding
                
            else: #else move normally
                gliding = False #you're not gliding
                glideStartPos = None #you're not gliding
                glideDir = None #you're not gliding
                state.pos += move[0] #Make the move you were trying to make

                #morier interp stuff
                lastPos = state.pos - move[0] #the position you were at before the move
                lastTime = move[1] #the time you started moving
                thisPos = state.pos #the position you're at after the move
                thisTime = move[1] + self.moveLength #the time you finish moving
                x = easeOutPow(lastPos.x, thisPos.x, lastTime, thisTime, 3, state.time) #your interpolated x position
                y = easeOutPow(lastPos.y, thisPos.y, lastTime, thisTime, 3, state.time) #your interpolated y position
                state.visiblePos = Vector2(x, y) #your visible position is the interpolated position

                if state.time > thisTime: #if you've passed the time when the interp ends
                    state.animState = "standing" #you're standing
                else: #else
                    state.animState = "walking" #you're still walking
                
                tile = level.getTileAt(state.pos, move[1]) #get the tile you moved to
                if tile is None or tile.type == "glidePath": #if you moved to nothing / a glide path
                    state.deathTime = move[1] #you died at the time of the move
                    state.animState = "dead" #you're dead at the time of the move
                    return state #so return the dead state
                
                state.movesMade += 1 #you made a move
                if tile.type != "rest": #if its not a rest tile, it affects your acc
                    state.accMovesMade += 1 #you made an acc affecting move
                    state.acc = calculateAcc(state.acc, state.accMovesMade, tile.appearedTime, move[1]) #update acc
                    state.offset = calculateOffset(state.offset, state.accMovesMade, tile.appearedTime, move[1]) #update offset
                
                currentTile = tile #Otherwise that's the tile you're on
            
        tile = level.getTileAt(state.pos, searchTime) #If your last move was made before the search time
        if tile != currentTile and not gliding: #if you're not on the tile that you were on after your last move
            state.deathTime = currentTile.disappearTime + level.disappearLength #then you died when that tile disappeared
            state.animState = "dead" #so you're dead
            return state #so return the dead state
        
        return state #return the alive state