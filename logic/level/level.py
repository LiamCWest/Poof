# external imports
import hashlib #for level encoding
import json #for level serialization

# internal imports
import graphics.gui as gui #for drawing
import logic.song.songPlayer as songPlayer #for methods
from logic.song.timingPoints import TimeSignature, TimingPoint #for timing point methods
from utils.vector2 import Vector2 #Vector2
from utils.polygon import Polygon #polygon for drawing
from objects.player import Player #Player
from objects.tile import Tile #Tile
from graphics.animation import * #Animation, AnimEvent, methods

class Level: #the level class
    deathTimeBuffer = 0.5 #the time after the player dies before the level restarts
    def __init__(self, tiles, appearLength, disappearLength, songPath, timingPoints, playerStartPos = None, playerStartTime = None): #constructor
        self.appearLength = appearLength #the time that tiles take to appear
        self.disappearLength = disappearLength #the time that tiles take to disappear
        
        tileEvents = [self.createEventFromTile(tile) for tile in tiles] #create the animation events from the tiles
        self.tileAnim = Animation(tileEvents, 0) #create the animation from the events
        self.pos = Vector2(0, 0) #the level pos, used in editor
        self.tileSize = Vector2(100, 100) #the size of a tile in pixels
        
        self.playerStartPos = playerStartPos #the position that the player starts at
        self.playerStartTime = playerStartTime #the time that the player starts at
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime) #makes the player
        
        self.songPath = songPath #the file path that the song is located at
        self.timingPoints = timingPoints #the timing points of the song
        songPlayer.load(self.songPath) #load the song
    
    def createEventFromTile(self, tile): #makes an animation event from a tile
        startTime = tile.appearedTime - self.appearLength #the start time of the event, starts when the tile starts appearing
        endTime = tile.disappearTime + self.disappearLength #the end time of the event, ends when the tile disappears
        callback = lambda t, win, topLeftPos, tileSize, tile=tile: tile.draw(win, topLeftPos, tileSize, self.appearLength, self.disappearLength, t + tile.appearedTime - self.appearLength) #the callback function, draws the tile
        data = tile #the data of the event, the tile
        return AnimEvent(startTime, endTime, callback, data) #construct the event
    
    def addTile(self, tile): #adds a tile to the level
        self.tileAnim.addEvent(self.createEventFromTile(tile)) #add the tile event to the animation
        
    def removeTileAt(self, pos, levelTime): #removes a tile located at a specific position and time from the level
        for i in self.tileAnim.tree.at(levelTime): #iterate through the events at the time
            tile = i.data[1] #get the tile
            if tile.pos == pos: #if the tile is at the position
                self.tileAnim.tree.remove(i) #remove the event from the tree
    
    def createPlayer(self, playerStartPos, playerStartTime): #creates a player
        if playerStartPos is not None and playerStartTime is not None: #if the player start position and time are not none
            return Player(playerStartPos, playerStartTime) #create the player
        return None #else return none
    
    def restart(self): #restarts the level (called when the player dies)
        self.pos = Vector2(0, 0) #reset the level pos
        
        self.player = self.createPlayer(self.playerStartPos, self.playerStartTime) #reset the player
        
        songPlayer.seek(0) #seek to the start of the song
        songPlayer.unpause() #play the song again
        self.tileAnim.restart(songPlayer.getPos()) #restart the tile animation        
    
    def draw(self, win, timeSourceTime, topLeftPos, tileSize, drawPlayer = False, freezeTilesOnDeath = False, playerState = None, drawGrid = False, gridLineThickness = 2): #draws the level with various params       
        if drawPlayer and freezeTilesOnDeath and playerState.deathTime is not None and playerState.deathTime < timeSourceTime: #if the player is dead and the tiles should be frozen
            levelTime = playerState.deathTime #set the level time to the time the player died
        else: #else
            levelTime = timeSourceTime #set the level time to the time passed in
        
        self.tileAnim.updateTime(levelTime, win, topLeftPos, tileSize) #update the tile animation
        
        if self.player is not None and drawPlayer: #if there is a player and you have to draw it
            self.player.draw(win, playerState) #draw the player
        
        if drawGrid: #if you have to draw the grid
            ltHalf = gridLineThickness / 2 #half the line thickness
            screenSize = Vector2(gui.screen.get_size()[0], gui.screen.get_size()[1]) #the size of the screen in pixels
            topLeftMod = self.tilePosToScreenPos(topLeftPos, Vector2(0, 0)) % tileSize #the position of the top left grid space
            
            gridWidth = screenSize.x + tileSize.x #the width of the grid
            gridHeight = screenSize.y + tileSize.y #the height of the grid
            for i in range(math.floor(screenSize.x / tileSize.x) + 2): #draw the vertical lines
                pos = topLeftMod - tileSize + (Vector2(i, 0) * tileSize) #get the position of the line
                polygon1 = Polygon.fromRect((pos.x - ltHalf, pos.y - ltHalf, gridLineThickness, gridHeight)) #make a polygon from the line
                polygon1.draw(win) #draw the polygon
                
            for i in range(math.floor(screenSize.y / tileSize.y) + 2): #draw the horizontal lines
                pos = topLeftMod - tileSize + (Vector2(0, i) * tileSize) #get the position of the line
                polygon1 = Polygon.fromRect((pos.x - ltHalf, pos.y - ltHalf, gridWidth, gridLineThickness)) #make a polygon from the line
                polygon1.draw(win) #draw the polygon
            
    def getTileAt(self, pos, levelTime): #gets the tile at a specific position and time
        for i in self.tileAnim.tree.at(levelTime): #iterate through the events at the time
            tile = i.data[1] #get the tile
            if tile.pos == pos: #if the tile is at the position
                return tile #return the tile
        return None #else return none
    
    def getTilesOverlapping(self, pos, startTime, endTime): #gets the tiles overlapping a specific position and time range
        tiles = [] #the tiles
        for i in self.tileAnim.tree.overlap(startTime, endTime): #iterate through the events overlapping the time range
            tile = i.data[1] #get the tile
            if tile.pos == pos: #if the tile is at the position
                tiles.append(tile) #add the tile to the list
        tiles.sort(key=lambda tile: tile.appearedTime) #sort the tiles by the time they appear
        return tiles #return the tiles
            
    def isTileValid(self, tile, oldTile): #checks if a tile is valid to be added to the level
        if tile.appearedTime < 0 or tile.disappearTime < 0 or tile.appearedTime > songPlayer.getSongLength(): #if the tile appears or disappears before the song starts or after the song ends
            return False #return false
        if tile.appearedTime > tile.disappearTime: #if the tile appears after it disappears
            return False #return false
        overlapping = self.tileAnim.tree.overlap(tile.appearedTime, tile.disappearTime) #get the tiles overlapping the time range
        for i in overlapping: #iterate through the tiles
            if i.data[1].pos == tile.pos and i.data[1] != oldTile: #if the tile is at the same position as the tile being added and it is not the same tile
                return False #return false
        return True #return true

    def save(self, levelFile): #saves the level to a file
        tileValues = [event.data[1].toValues() for event in self.tileAnim.tree] #array-ify all the tiles
        noV2sTiles = [[tile[0].toTuple(), tile[1], tile[2], tile[3], tile[4], tile[5]] for tile in tileValues] #convert all the vector2s to tuples
    
        timingPoints = [point.toValues() for point in self.timingPoints] #array-ify all the timing points
            
        levelData = { #make a dictionary of the level data
            "tiles": noV2sTiles, #the tiles
            "appearLength": self.appearLength, #the tile appear length
            "disappearLength": self.disappearLength, #the tile disappear length
            "songPath": self.songPath, #the song file path
            "timingPoints": timingPoints, #the timing points
            "playerStartPos": self.playerStartPos.toTuple(), #the player start position
            "playerStartTime": self.playerStartTime #the player start time
            }
        
        signature = signData(levelData) #get the signature of the level data
        
        with open(levelFile, 'w') as file: #open the file
            json.dump({"data": levelData, "signature": signature}, file) #dump the level data to the file
            
    def screenPosToTilePos(self, screenPos, topLeftPos): #converts a screen position to a tile position
        return screenPos / self.tileSize + topLeftPos #divide the screen position by the tile size and add the top left position
    
    def screenPosToRoundedTilePos(self, screenPos, topLeftPos): #converts a screen position to a floored tile position
        tilePos = screenPos / self.tileSize + topLeftPos #divide the screen position by the tile size and add the top left position 
        return Vector2(math.floor(tilePos.x), math.floor(tilePos.y)) #floor both components of the tile position
    
    def tilePosToScreenPos(self, tilePos, topLeftPos): #converts a tile position to a screen position
        return self.tileSize * (topLeftPos - tilePos) #multiply the tile size by the difference between the top left position and the tile position
    
    def getEndTime(self): #gets the end time of the level (the time when the last tile starts disappearing)
        return math.nextafter(self.tileAnim.tree.end(), float("-inf")) - self.disappearLength #the time when the last time is fully disappeared - the time that it takes to disappear
    
    def getEndPositions(self): #gets the positions of all the tiles at the end of the level
        endIntervals =  self.tileAnim.tree.at(math.nextafter(self.tileAnim.tree.end(), float("-inf"))) #get the tiles that disappear last
        endTiles = [i.data[1].pos for i in endIntervals] #get the positions of the tiles
        return endTiles #return the positions
    
    @classmethod #class method
    def fromFile(cls, levelFile): #loads a level from a file
        with open(levelFile, 'r') as file: #open the file
            saved_data = json.load(file) #load the data from the file
            loaded_data = saved_data['data'] #get the level data
            saved_signature = saved_data['signature'] #get the signature
            if not checkSignature(loaded_data, saved_signature): #check if the signature is valid
                print("Level file corrupted") #print error
                return None #return no level
            tiles = loaded_data['tiles'] #get the tiles
            tilesV2 = [Tile(Vector2.from_tuple(tile[0]), tile[1], tile[2], tile[3], tile[4], tile[5]) for tile in tiles] #convert the tiles to tile objects
            appearLength = loaded_data['appearLength'] #get the tile appear length
            disappearLength = loaded_data['disappearLength'] #get the tile disappear length
            songPath = loaded_data['songPath'] #get the song file path
            timingPointsVals = loaded_data['timingPoints'] #get the timing points
            timingPoints = [TimingPoint(timingPoint[0], timingPoint[1], TimeSignature(timingPoint[2], timingPoint[3])) for timingPoint in timingPointsVals] #convert the timing points to timing point objects
            playerStartPos = Vector2.from_tuple(loaded_data['playerStartPos']) #get the player start position
            playerStartTime = loaded_data['playerStartTime'] #get the player start time
            level = cls(tilesV2, appearLength, disappearLength, songPath, timingPoints, playerStartPos, playerStartTime) #create the level
            return level #return the level

def signData(data): #signs the data
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest() #hash the data
    return signature #return the signature

def checkSignature(data, signature): #checks if the signature is valid
    return signature == signData(data) #checks if the new signature is equal to the stored signature