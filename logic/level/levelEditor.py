#the level editor screen

# external imports
import pygame # import pygame as it is used for base game functionality
import bisect # import bisect to add things to the middle of lists
import math # import math for additional mathimatical functions

# internal imports
import input.input as input # import the input file for checking if keys are pressed
import graphics.gui as gui # import the gui file to get the screen to draw to
import logic.song.songPlayer as songPlayer # import the songPlayer file for song functions
import logic.song.timingPoints as timingPoints # import the timingPoints file for timingPoint functions
from logic.song.timingPoints import TimingPoint, TimeSignature # import TimingPoint and TimeSignature from the timing points file
from logic.level.level import Level # import the Level class
from objects.tile import Tile # import the Tile class
from ui.button import Button # import the Button class
from ui.toolbar import Toolbar, ToolbarOption # import the Toolbar and ToolbarOptions classes
from ui.inputBox import InputBox # import the InputBox class
from ui.text import Text # import the Text class
from ui.scrollbar import Scrollbar # import the Scrollbar class
from utils.vector2 import Vector2 # import the Vector2 class
from utils.polygon import Polygon # import the Polygon clasa

popupOpen = False # if the level editor has an open popup (not used, only because gui calls it)
hColor = (150, 150, 255) # color of the highlight on buttons

# select mode of input (move, select, platform, rest, glide, glide path, delete)
def selectMode(option):
    global selectedMode # global variable for the selected mode
    topBar.objects[modes.index(selectedMode)].baseObj.color = (100, 100, 255) # set the color of the previously selected mode to the default
    selectedMode = option # set the selected mode to the new mode
    topBar.objects[modes.index(selectedMode)].baseObj.color = (50, 50, 255) # set the color of the newly selected mode to the selected color

# select divisor for the level editor, divisor is what length of tile you are placing
def selectDivisor(d):
    global divisor # global variable for the divisor
    divisorSelector[divisors.index(divisor)].color = (100, 100, 255) # set the color of the previously selected divisor to the default
    divisor = d # set the divisor to the new divisor
    divisorSelector[divisors.index(d)].color = (50, 50, 255) # set the color of the newly selected divisor to the selected color

selectedTile = None # the currently selected tile
# check for input
def checkInput():
    global level, divisor, selectedTile # global variables for the level, divisor, and selected tile
    # check for play keybind input to play/pause the song
    if input.keyActionBindings["play"].justPressed:
        if songPlayer.getIsPlaying(): # if the song is playing, pause it
            songPlayer.pause() # pause the song
            songPlayer.seek(timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor)) # seek to the nearest beat
        else: #else
            # if the song is paused, play it
            songPlayer.unpause()
    
    # check for input to move the selected tile
    if selectedTile:
        if input.keyActionBindings["moveTileLeft"].justPressed: # if the move tile left keybind is pressed
            selectedTile.pos += Vector2(-1, 0) # move the tile left
        if input.keyActionBindings["moveTileRight"].justPressed: # if the move tile right keybind is pressed
            selectedTile.pos += Vector2(1, 0) # move the tile right
        if input.keyActionBindings["moveTileUp"].justPressed: # if the move tile up keybind is pressed
            selectedTile.pos += Vector2(0, -1) # move the tile up
        if input.keyActionBindings["moveTileDown"].justPressed: # if the move tile down keybind is pressed
            selectedTile.pos += Vector2(0, 1) # move the tile down
        
        # check for input to change the length of the selected tile
        if input.keyActionBindings["increaseTileLength"].justPressed: # if the increase tile length keybind is pressed
            newTileEndTime = timingPoints.getNextBeat(level.timingPoints, selectedTile.disappearTime, divisor) # get the next note point (beat/divisor)
            newTile = selectedTile.copy() # copy the selected tile to prevent changing the original tile
            newTile.disappearTime = newTileEndTime # set the disappear time of the new tile to the next note point (beat/divisor)
            if level.isTileValid(newTile, selectedTile): # if the new tile is valid
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime) # remove the old tile
                selectedTile = newTile.copy() # set the selected tile to the new tile
                level.addTile(selectedTile) # add the new tile to the level
        if input.keyActionBindings["decreaseTileLength"].justPressed: # if the decrease tile length keybind is pressed
            newTileEndTime = timingPoints.getPreviousBeat(level.timingPoints, selectedTile.disappearTime, divisor) # get the previous note point (beat/divisor)
            if newTileEndTime >= selectedTile.appearedTime: # if the new tile end time is greater than the selected tile appeared time
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime) # remove the old tile
                selectedTile.disappearTime = newTileEndTime # set the disappear time of the selected tile to the new tile end time
                level.addTile(selectedTile) # add the selected tile to the level

    # check for input to change song time
    if input.keyActionBindings["timeForwards"].justPressed: # if the time forwards keybind is pressed
        oldTime = songPlayer.getPos() # set old time to current song time
        songPlayer.seek(min(timingPoints.getNextBeat(level.timingPoints, oldTime, divisor), songPlayer.getSongLength())) # go to next note point (beat/divisor)
        #delta = songPlayer.getPos() - oldTime
        #if selectedTile:                  TURNS OUT TO BE QUITE ANNOYING TO MAKE A LEVEL AND YOUR TILES MOVE ON YOU
        #    newTile = selectedTile.copy()
        #    newTile.appearedTime += delta
        #    newTile.disappearTime += delta
        #    if level.isTileValid(newTile, selectedTile):
        #        level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
        #        selectedTile = newTile.copy()
        #        level.addTile(selectedTile)
        
    if input.keyActionBindings["timeBackwards"].justPressed: # if the time backwards keybind is pressed
        oldTime = songPlayer.getPos() # set old time to current song time
        songPlayer.seek(max(0, timingPoints.getPreviousBeat(level.timingPoints, oldTime, divisor))) # go to previous note point (beat/divisor)
        #delta = songPlayer.getPos() - oldTime
        #if selectedTile:
        #    newTile = selectedTile.copy()
        #    newTile.appearedTime += delta
        #    newTile.disappearTime += delta
        #    if level.isTileValid(newTile, selectedTile):
        #        level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
        #        selectedTile = newTile.copy()
        #        level.addTile(selectedTile)

levelPos = Vector2(0, 0) # position of the level relative to the screen, for mouse panning
# update function for the level editor
def update(): 
    checkInput() # check for inputs
    metronomeUpdate() # update the metronome oject
    timingPointUpdate() # update the timingPoint input boxes
    inBoxUpdate() # update the general input box
    topBar.update() # update the top toolbar 
    bottomBar.update() # update the bottom tool bar
    
    global lastScrollbarValue, divisor # global variables for the lastScrollbarValue and divisor
    songLen = songPlayer.getSongLength() # set the songLength variable to the song length
    if scrollbar.getValue() != lastScrollbarValue: # if the current scrollbar value is not the last scrollbar value, changne position in the song
        songPos = songLen * scrollbar.getValue() # set the song pos to the song pos from the scrollbar value
        roundedSongPos = timingPoints.getNearestBeat(level.timingPoints, songPos, divisor) #get the time of the nearest beat
        songPlayer.seek(roundedSongPos) # seek to the nearest beat
        scrollbar.moveTo(roundedSongPos / songLen) # move the scrollbar to the nearest beat
    else: #else
        scrollbar.moveTo(songPlayer.getPos() / songLen) # move the scrollbar to the current song position
    lastScrollbarValue = scrollbar.getValue() # update the last scrollbar value

    if not posIn(input.mousePos.pos, topBar.getRect()) and input.mousePos.pos.y < bottomBar.pos.y: # if the mouse is not in the top bar or the bottom bar
        global lastMousePos, levelPos, selectedTile #global variables
        if selectedMode == "move" and input.mouseBindings["lmb"].pressed: #if you're moving the level
            currentMousePos = input.mousePos.pos # set the current mouse position to the mouse position
            levelPos -= (currentMousePos - lastMousePos) / level.tileSize # move the level position by the difference in mouse position
            lastMousePos = currentMousePos #update the last mouse position
        else: #else
            lastMousePos = input.mousePos.pos #update the last mouse position
            
        if selectedMode == "select" and input.mouseBindings["lmb"].justPressed: #if you're selecting a tile
            selectedTile = level.getTileAt(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), songPlayer.getPos()) #select the tile under your mouse
        
        if selectedMode in ["platform", "glide", "glide\npath", "rest"] and input.mouseBindings["lmb"].justPressed: #if you're placing a tile
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos) #get the position of the tile
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor) #get the time of the nearest beat
            if level.getTileAt(tilePos, tileTime) is None: #if there is no tile at that position
                tile = Tile(tilePos, None, tileTime, tileTime, selectedMode) #create a tile
                if selectedMode == "glide": #if you're placing a glide tile
                    tile.divisor = 1 #set the divisor to 1 by default
                if selectedMode == "glide\npath": #if you're placing a glide path tile
                    tile.type = "glidePath" #set the type to glidePath instead of glide\npath
                level.addTile(tile) #add the tile to the level
                selectedTile = level.getTileAt(tilePos, tileTime) #select the tile you just placed
            
        if selectedMode == "delete" and input.mouseBindings["lmb"].justPressed: #if you're deleting a tile
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos) #get the position of the tile
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor) #get the time of the nearest beat
            level.removeTileAt(tilePos, tileTime) #remove the tile at that position
            selectedTile = None #unselect the tile

lastInput = "" #the last input to the input box
lastTile = None #the last tile selected
def inBoxUpdate(): #update the input box
    global lastInput, lastTile, inBox #globals
    if selectedTile and selectedTile.type == "glide": #if you're selecting a glide tile
        if lastInput != inBox.output and inBox.output != "" and selectedTile == lastTile: #if the input has changed and it's not empty and you're still selecting the same tile
            if all(c.isdigit() for c in inBox.output): #if the input is a number
                selectedTile.divisor = int(inBox.output) #set the divisor to the input
            else: #else
                inBox.changeText(str(selectedTile.divisor)) #reset the inputbox to the tile divisor
        elif selectedTile != lastTile: #else if you're selecting a different tile
            inBox.changeText(str(selectedTile.divisor)) #reset the inputbox to the tile divisor
    else: #else
        inBox.changeText("") #reset the inputbox to empty
        
    lastInput = inBox.output #update the last input
    lastTile = selectedTile #update the last tile

lastTimingPoint = None #the last timing point selected
def timingPointUpdate(): #update the timing point input boxes
    global bpm, timeSig, divisor, lastTimingPoint #globals
    pos = songPlayer.getPos() #get the current song position
    nearestBeat = timingPoints.getNearestBeat(level.timingPoints, pos, divisor) #get the time of the nearest beat
    point = timingPoints.getPreviousPoint(level.timingPoints, pos) #get the previous timing point
    if point is None: #if there is no previous timing point
        point = level.timingPoints[0] #set the timing point to the first timing point
        
    pointChanged = point != lastTimingPoint #if the timing point has changed
    if pointChanged: #if the timing point has changed
        adjustTimingPointValues() #update the timing point input boxes
    
    #if you're updating the timing point
    changingPoint = (int(bpm[1].output) != point.bpm or #if the bpm has changed
        int(timeSig[0].output) != point.timeSignature.num or #or the time signature numerator has changed
        int(timeSig[1].output) != point.timeSignature.denom) and not pointChanged #or the time signature denominator has changed and the timing point hasn't changed
    
    lastTimingPoint = point #update the last timing point
    
    if nearestBeat == point.time: #if you're on a timing point
        if changingPoint: #if you're updating the timing point
            point.bpm = int(bpm[1].output) #set the bpm to the input
            point.timeSignature.num = int(timeSig[0].output) #set the time signature numerator to the input
            point.timeSignature.denom = int(timeSig[1].output) #set the time signature denominator to the input
            
        onPointColor = (50, 50, 255) #color of the timing point input boxes when you're on a timing point
        bpm[0].bgColor = onPointColor #set the bpm text background color to the on point color
        bpm[1].color = onPointColor #set the bpm input box color to the on point color
        timeSig[0].color = onPointColor #set the time signature numerator input box color to the on point color
        timeSig[1].color = onPointColor #set the time signature denominator input box color to the on point color
    else: #else
        if changingPoint: #if you're updating the timing point
            pointToInsert = TimingPoint(songPlayer.getPos(), int(bpm[1].output), TimeSignature(int(timeSig[0].output), int(timeSig[1].output))) #insert a new timing point at the time
            bisect.insort_left(level.timingPoints, pointToInsert, key=lambda point: point.time) #insert the timing point into the timing points list at its proper position
            
        offPointColor = (100, 100, 255) #color of the timing point input boxes when you're not on a timing point
        bpm[0].bgColor = offPointColor #set the bpm text background color to the off point color
        bpm[1].color = offPointColor #set the bpm input box color to the off point color
        timeSig[0].color = offPointColor #set the time signature numerator input box color to the off point color
        timeSig[1].color = offPointColor #set the time signature denominator input box color to the off point color

def metronomeUpdate(): #update the metronome
    pos = songPlayer.getPos() #get the current song position
    point = timingPoints.getPreviousPoint(level.timingPoints, pos) #get the previous timing point
    if point is None: #if there is no previous timing point
        point = level.timingPoints[0] #set the timing point to the first timing point
        
    if len(metronome) != point.timeSignature.num + 1: #if the length of the metronome is not the same as the time signature
        genMetronome() #regenerate the metronome
        
    if pos < point.time: #if you're before the timing point
        selectMetBeat(0) #select the first beat
        return #stop the function

    beatsSincePoint = timingPoints.getBeatsSincePoint(pos, point, 1) #else get the number of beats since the timing point
    selectMetBeat(beatsSincePoint % point.timeSignature.num) #select the corresponding beat
            
def selectMetBeat(b): #select a beat in the metronome
    global beat, metronome #globals
    for i, met in enumerate(metronome[:-1]): #for each beat in the metronome
        if i == b: #if it's the selected beat
            met.color = (50, 50, 255) if b != 0 else (150, 150, 255) #set the color to the selected color
        else: #else
            met.color = (100, 100, 255) #set the color to the deselected color

    metronome[-1].x = metronome[b].pos.x #set the x position of the metronome text to the pos of the selected beat box
    metronome[-1].text = str(b + 1) #set the text of the metronome text to the selected beat number

def posIn(pos, rect): #check if a position is in a rectangle
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3] #return if the position is in the rectangle
    
def draw(): #draw the level editor
    global levelPos, selectedTile #globals
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, drawGrid=True) #draw the level, dont draw player, do draw grid
    
    if selectedTile and selectedTile.appearedTime-level.appearLength <= songPlayer.getPos() <= selectedTile.disappearTime+level.disappearLength: #if the selected tile is on screen
        s = pygame.Surface(level.tileSize.toTuple()) #create a surface
        s.set_alpha(128) #make it semitransparent
        s.fill((255,255,255)) #fill it white
        gui.screen.blit(s, ((selectedTile.pos - levelPos) * level.tileSize).toTuple()) #draw it to the screen
    elif selectedTile: #else if the selected tile is not on screen
        selectedTile = None #unselect the tile
    
    topBar.draw(gui.screen) #draw the top bar
    bottomBar.draw(gui.screen) #draw the bottom bar
        
level = None #the level being edited
lastMousePos = Vector2(0, 0) #the last mouse position
def show(): #show the level editor
    global lastMousePos #globals
    init() #initialize the level editor
    lastMousePos = input.mousePos.pos #set the last mouse position to the current mouse position
    
    update() #update the level editor

def loadLevel(levelFile): #load the level
    global level, levelF #globals
    levelF = levelFile #set the level file to the level file
    songPlayer.unload() #unload the song
    level = Level.fromFile(levelFile) #load the level from the file

def adjustTimingPointValues(): #adjust the timing point input boxes
    global timeSig, bpm #globals
    pos = songPlayer.getPos() #get the current song position
    point = timingPoints.getPreviousPoint(level.timingPoints, pos) #get the previous timing point
    if point is None: #if there is no previous timing point
        point = level.timingPoints[0] #set the timing point to the first timing point
        
    bpm[1].changeText(str(point.bpm)) #set the bpm input box to the bpm of the timing point
    timeSig[0].changeText(str(point.timeSignature.num)) #set the time signature numerator input box to the time signature numerator of the timing point
    timeSig[1].changeText(str(point.timeSignature.denom)) #set the time signature denominator input box to the time signature denominator of the timing point

def genMetronome(): #generate the metronome
    global metronome, metronomeSize, bottomBar #globals
    pos = songPlayer.getPos() #get the current song position
    point = timingPoints.getPreviousPoint(level.timingPoints, pos) #get the previous timing point
    if point is None: #if there is no previous timing point
        point = level.timingPoints[0] #set the timing point to the first timing point
    metronomeLen = point.timeSignature.num # length of a measure
    metronome = [] #list of metronome beats
    metronomeSize = bottomBar.width/(3*metronomeLen) #size of a metronome beat
    if metronomeSize > buttonSize/2: metronomeSize = buttonSize/2 #if the metronome size is too big, make it smaller
    for i in range(metronomeLen): #for each beat in the metronome
        metronome.append(Polygon.fromRect((i*metronomeSize, (buttonSize/2-metronomeSize)/2, metronomeSize, metronomeSize), (100, 100, 255))) #create a polygon
    metronome.append(Text("1", metronomeSize/2, metronomeSize/2+(buttonSize/2-metronomeSize)/2, (0,0,0), round(metronomeSize*0.66), width=metronomeSize, height=metronomeSize, font="Encode Sans")) #create the metronome text
    if bottomBar.grid[0][2]: #if there is already a metronome
        bottomBar.grid[0][2].baseObj = metronome #set the thing in the toolbar that should be a metronome to the metronome

def deletePoint(): #delete the current timing point
    global level #globals
    prevPoint = timingPoints.getPreviousPoint(level.timingPoints, songPlayer.getPos()) #get the previous timing point
    point = prevPoint if prevPoint else level.timingPoints[0] #set the timing point to the previous timing point if there is one, else set it to the first timing point
    level.timingPoints.remove(point) #remove the timing point from the timing points list

initailized = False #if the level editor has been initialized
def init(): #initialize the level editor
    global topBar, bottomBar, modes, divisorSelector, divisors, scrollbar, selectedMode, divisor, initailized, lastScrollbarValue, metronome, metronomeSize, buttonSize, bpm, timeSig, inBox #globals
    if initailized: return #if the level editor has already been initialized, stop the function
    initailized = True #set the level editor to initialized
    # vars
    buttonSize = 90 #size of the top toolbar buttons
    lastScrollbarValue = 0 #last value of the scrollbar
    fontSize = 20 #font size of the top toolbar stuff

    # top bar #
    numButtons = 11 # number of buttons on the top bar
    w = buttonSize*numButtons # width of the top bar
    topBar = Toolbar(Vector2(numButtons, 1), Vector2((gui.screen.get_width()-w)//2, 0), w, buttonSize) # toolbar for the top bar

    modes = ["move", "select", "platform", "rest", "glide", "glide\npath", "delete"] # possible modes
    topbarButtons = { # buttons on the top bar
        "save": lambda: level.save(levelF), # function for save button
        "delete\npoint": lambda: deletePoint(), #function for delete point button
    }
    bpmText = Text("BPM", buttonSize/2, buttonSize/4, (0,0,0), fontSize, bgColor=(100, 100, 255), width = buttonSize, height = buttonSize/2, font="Encode Sans") # text for bpm
    bpmBox = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for bpm
    bpm = [bpmText, bpmBox] # bpm text and input box
    timeSigNum = InputBox("", 0, 0, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for time signature numerator
    timeSigDenom = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for time signature denominator
    timeSig = [timeSigNum, timeSigDenom] # time signature numerator and denominator

    # fuction to create buttons for the toolbar, could probably be moved somewhere else. ToolbarOption.fromButton?
    def barButton(option, func): #creates a button for the toolbar
        return Button( #creates a button
            option, 0, 0, buttonSize, buttonSize, (100, 100, 255), #some parameters
            (0, 0, 0), onRelease=func, textSize = fontSize, scaler=1, hColor=hColor, textFont="Encode Sans" #some more parameters
        ) #closing bracket for the button

    # adding modes and buttons to the toolbar
    for i, mode in enumerate(modes): #for each mode
        topBar.addOption(ToolbarOption(mode, barButton(mode, lambda x=mode: selectMode(x))), Vector2(i, 0)) #add a button for the mode
    for button in topbarButtons.keys(): #add a button for save and load
        i += 1 #increment i for each button
        topBar.addOption(ToolbarOption(button, barButton (button, topbarButtons[button])), Vector2(i, 0)) #add buttons for save and load
    selectedMode = "move" #set the selected mode to move
    selectMode("move") #select the move mode

    # add bpm and time signature to the top bar
    i += 1 #increment i
    topBar.addOption(ToolbarOption(bpm, bpm), Vector2(i, 0)) #add an option for the bpm
    i += 1 #increment i
    topBar.addOption(ToolbarOption(timeSig, timeSig), Vector2(i, 0)) #add an option for the time signature

    # bottom bar #
    bottomBar = Toolbar(Vector2(3, 2), Vector2(0, gui.screen.get_height()-buttonSize), gui.screen.get_width(), buttonSize) # toolbar for the bottom bar

    scrollbar = Scrollbar(0, 0, bottomBar.height/2, gui.screen.get_width(), "h", sliderWidth=25, bg = (50,50,50)) # scrollbar for the bottom bar

    divisor = 1 # divisor for the level editor
    divisors = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16] #all possible divisors
    divisorSelector = [] #list of divisor buttons
    divisorSize = bottomBar.width/(3*len(divisors)) #size of a divisor button
    if divisorSize > buttonSize/2: divisorSize=buttonSize/2 #if the divisor size is too big, make it smaller
    for i, d in enumerate(divisors): #for each divisor
        divisorSelector.append(Button(str(d), math.floor(i*divisorSize), math.floor((buttonSize/2-divisorSize)/2), math.ceil(divisorSize), math.ceil(divisorSize), (100, 100, 255), (0,0,0), onRelease=lambda x=d: selectDivisor(x), textSize = 30, scaler=1, hColor=hColor, textFont="Encode Sans")) #create a button
    selectDivisor(1) #select the first divisor
    
    inBoxWidth = math.floor(bottomBar.width/3)-10 #width of the input box
    inBoxHeight = math.floor(bottomBar.height/2)-6 #height of the input box
    inBox = InputBox("", 5, 3, inBoxWidth, inBoxHeight, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") #input box for the glide divisor
    
    genMetronome() #generate the metronome
    selectMetBeat(1) #select the first beat
    
    #adding to bottom bar
    bottomBar.addOption(ToolbarOption("scrollbar", scrollbar), Vector2(0,1)) #add the scrollbar to the bottom bar
    bottomBar.addOption(ToolbarOption("divisor", divisorSelector), Vector2(0,0)) #add the divisor buttons to the bottom bar
    bottomBar.addOption(ToolbarOption("inBox", inBox), Vector2(1,0)) #add the input box to the bottom bar
    bottomBar.addOption(ToolbarOption("metronome", metronome), Vector2(2,0)) #add the metronome to the bottom bar
    
    adjustTimingPointValues() #update the timing point input boxes

def hide(): #hide the level editor
    global selectedTile, lastTimingPoint, initailized #globals
    gui.clear() #clear the screen
    songPlayer.unload() #unload the song
    initailized = False #set the level editor to not initialized
    selectedTile = None #unselect the tile
    lastTimingPoint = None #reset the last timing point