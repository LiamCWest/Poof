# external imports
import pygame # import pygame as it is used for base game functionality
import bisect # import bisect to add things to the middle of lists
import math # import maath for additional mathimatical functions

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
        else:
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
    if input.keyActionBindings["timeForwards"].justPressed:
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
        
    if input.keyActionBindings["timeBackwards"].justPressed:
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
        songPos = songLen * scrollbar.getValue() # 
        roundedSongPos = timingPoints.getNearestBeat(level.timingPoints, songPos, divisor)
        songPlayer.seek(roundedSongPos)
        scrollbar.moveTo(roundedSongPos / songLen)
    else: 
        scrollbar.moveTo(songPlayer.getPos() / songLen)
    lastScrollbarValue = scrollbar.getValue()

    if not posIn(input.mousePos.pos, topBar.getRect()) and input.mousePos.pos.y < bottomBar.pos.y:
        global lastMousePos, levelPos, selectedTile
        if selectedMode == "move" and input.mouseBindings["lmb"].pressed:
            currentMousePos = input.mousePos.pos
            levelPos -= (currentMousePos - lastMousePos) / level.tileSize
            lastMousePos = currentMousePos
        else:
            lastMousePos = input.mousePos.pos
            
        if selectedMode == "select" and input.mouseBindings["lmb"].justPressed:
            selectedTile = level.getTileAt(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), songPlayer.getPos())
        
        if selectedMode in ["platform", "glide", "glide\npath", "rest"] and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor)
            if level.getTileAt(tilePos, tileTime) is None:
                tile = Tile(tilePos, None, tileTime, tileTime, selectedMode)
                if selectedMode == "glide":
                    tile.divisor = 1
                if selectedMode == "glide\npath":
                    tile.type = "glidePath"
                level.addTile(tile)
                selectedTile = level.getTileAt(tilePos, tileTime)
            
        if selectedMode == "delete" and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor)
            level.removeTileAt(tilePos, tileTime)
            selectedTile = None

lastIn = ""
lastTile = None
def inBoxUpdate():
    global lastIn, lastTile, inBox
    if selectedTile and selectedTile.type == "glide":
        if lastIn != inBox.output and inBox.output != "" and selectedTile == lastTile:
            if all(c.isdigit() for c in inBox.output):
                selectedTile.divisor = int(inBox.output)
            else:
                inBox.changeText(str(selectedTile.divisor))
        elif selectedTile != lastTile:
            inBox.changeText(str(selectedTile.divisor))
    else:
        inBox.changeText("")
        
    lastIn = inBox.output
    lastTile = selectedTile

lastTimingPoint = None
def timingPointUpdate():
    global bpm, timeSig, divisor, lastTimingPoint
    pos = songPlayer.getPos()
    nearestBeat = timingPoints.getNearestBeat(level.timingPoints, pos, divisor)
    point = timingPoints.getPreviousPoint(level.timingPoints, pos)
    if point is None:
        point = level.timingPoints[0]
        
    pointChanged = point != lastTimingPoint
    if pointChanged:
        adjustTimingPointValues()
    
    changingPoint = (int(bpm[1].output) != point.bpm or 
        int(timeSig[0].output) != point.timeSignature.num or
        int(timeSig[1].output) != point.timeSignature.denom) and not pointChanged
    
    lastTimingPoint = point
    
    if nearestBeat == point.time:
        if changingPoint:
            point.bpm = int(bpm[1].output)
            point.timeSignature.num = int(timeSig[0].output)
            point.timeSignature.denom = int(timeSig[1].output)
            
        onPointColor = (50, 50, 255)
        bpm[0].bgColor = onPointColor
        bpm[1].color = onPointColor
        timeSig[0].color = onPointColor
        timeSig[1].color = onPointColor            
    else:
        if changingPoint:
            pointToInsert = TimingPoint(songPlayer.getPos(), int(bpm[1].output), TimeSignature(int(timeSig[0].output), int(timeSig[1].output)))
            bisect.insort_left(level.timingPoints, pointToInsert, key=lambda point: point.time)
            
        offPointColor = (100, 100, 255)
        bpm[0].bgColor = offPointColor
        bpm[1].color = offPointColor
        timeSig[0].color = offPointColor
        timeSig[1].color = offPointColor

def metronomeUpdate(): #TODO: make beat number apear on each beat
    pos = songPlayer.getPos()
    point = timingPoints.getPreviousPoint(level.timingPoints, pos)
    if point is None:
        point = level.timingPoints[0]
        
    if len(metronome) != point.timeSignature.num + 1:
        genMetronome()
        
    if pos < point.time:
        selectMetBeat(0)
        return

    beatsSincePoint = timingPoints.getBeatsSincePoint(pos, point, 1)
    selectMetBeat(beatsSincePoint % point.timeSignature.num)
            
def selectMetBeat(b):
    global beat, metronome
    for i, met in enumerate(metronome[:-1]):
        if i == b:
            met.color = (50, 50, 255) if b != 0 else (150, 150, 255)
        else:
            met.color = (100, 100, 255)

    metronome[-1].x = metronome[b].pos.x
    metronome[-1].text = str(b + 1)

def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    global levelPos, selectedTile
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, drawGrid=True)
    
    if selectedTile and selectedTile.appearedTime-level.appearLength <= songPlayer.getPos() <= selectedTile.disappearTime+level.disappearLength:
        s = pygame.Surface(level.tileSize.toTuple())
        s.set_alpha(128)
        s.fill((255,255,255))
        gui.screen.blit(s, ((selectedTile.pos - levelPos) * level.tileSize).toTuple())
    elif selectedTile:
        selectedTile = None
    
    topBar.draw(gui.screen)
    bottomBar.draw(gui.screen)
        
tiles = None
level = None
lastMousePos = Vector2(0, 0)
def show():
    global lastMousePos
    init()
    lastMousePos = input.mousePos.pos
    
    update()
    
def loadLevel(levelFile):
    global level, levelF
    levelF = levelFile
    songPlayer.unload()
    level = Level.fromFile(levelFile)
    
def adjustTimingPointValues():
    global timeSig, bpm
    pos = songPlayer.getPos()
    point = timingPoints.getPreviousPoint(level.timingPoints, pos)
    if point is None:
        point = level.timingPoints[0]
        
    bpm[1].changeText(str(point.bpm))
    timeSig[0].changeText(str(point.timeSignature.num))
    timeSig[1].changeText(str(point.timeSignature.denom))

def genMetronome():
    global metronome, metronomeSize, bottomBar
    pos = songPlayer.getPos()
    point = timingPoints.getPreviousPoint(level.timingPoints, pos)
    if point is None:
        point = level.timingPoints[0]
    metronomeLen = point.timeSignature.num # length of a measure
    metronome = []
    metronomeSize = bottomBar.width/(3*metronomeLen)
    if metronomeSize > buttonSize/2: metronomeSize = buttonSize/2
    for i in range(metronomeLen):
        metronome.append(Polygon.fromRect((i*metronomeSize, (buttonSize/2-metronomeSize)/2, metronomeSize, metronomeSize), (100, 100, 255)))
    metronome.append(Text("1", metronomeSize/2, metronomeSize/2+(buttonSize/2-metronomeSize)/2, (0,0,0), round(metronomeSize*0.66), width=metronomeSize, height=metronomeSize, font="Encode Sans"))
    if bottomBar.grid[0][2]:
        bottomBar.grid[0][2].baseObj = metronome

def deletePoint():
    global level
    prevPoint = timingPoints.getPreviousPoint(level.timingPoints, songPlayer.getPos())
    point = prevPoint if prevPoint else level.timingPoints[0]
    level.timingPoints.remove(point)

initailized = False
def init():
    global topBar, bottomBar, modes, divisorSelector, divisors, scrollbar, selectedMode, divisor, initailized, lastScrollbarValue, metronome, metronomeSize, buttonSize, bpm, timeSig, inBox
    if initailized: return
    initailized = True
    # vars
    buttonSize = 90
    lastScrollbarValue = 0
    fontSize = 20

    # top bar #
    numButtons = 11
    w = buttonSize*numButtons # width of the top bar
    topBar = Toolbar(Vector2(numButtons, 1), Vector2((gui.screen.get_width()-w)//2, 0), w, buttonSize) # toolbar for the top bar

    modes = ["move", "select", "platform", "rest", "glide", "glide\npath", "delete"] # possible modes
    topbarButtons = { # buttons on the top bar
        "save": lambda: level.save(levelF), 
        "delete\npoint": lambda: deletePoint(),
    }
    bpmText = Text("BPM", buttonSize/2, buttonSize/4, (0,0,0), fontSize, bgColor=(100, 100, 255), width = buttonSize, height = buttonSize/2, font="Encode Sans") # text for bpm
    bpmBox = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for bpm
    bpm = [bpmText, bpmBox] # bpm text and input box
    timeSigNum = InputBox("", 0, 0, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for time signature numerator
    timeSigDenom = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans") # input box for time signature denominator
    timeSig = [timeSigNum, timeSigDenom] # time signature numerator and denominator

    # fuction to create buttons for the toolbar, could probably be moved somewhere else. ToolbarOption.fromButton?
    barButton = lambda option, func: Button(
        option, 0, 0, buttonSize, buttonSize, (100, 100, 255), 
        (0, 0, 0), onRelease=func, textSize = fontSize, scaler=1, hColor=hColor, textFont="Encode Sans"
    )
    # adding modes and buttons to the toolbar
    for i, mode in enumerate(modes):
        topBar.addOption(ToolbarOption(mode, barButton(mode, lambda x=mode: selectMode(x))), Vector2(i, 0))
    for button in topbarButtons.keys():
        i += 1
        topBar.addOption(ToolbarOption(button, barButton(button, topbarButtons[button])), Vector2(i, 0))
    selectedMode = "move"
    selectMode("move")

    # add bpm and time signature to the top bar
    i += 1
    topBar.addOption(ToolbarOption(bpm, bpm), Vector2(i, 0))
    i += 1
    topBar.addOption(ToolbarOption(timeSig, timeSig), Vector2(i, 0))

    # bottom bar #
    bottomBar = Toolbar(Vector2(3, 2), Vector2(0, gui.screen.get_height()-buttonSize), gui.screen.get_width(), buttonSize) # toolbar for the bottom bar

    scrollbar = Scrollbar(0, 0, bottomBar.height/2, gui.screen.get_width(), "h", sliderWidth=25, bg = (50,50,50)) # scrollbar for the bottom bar

    divisor = 1
    divisors = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
    divisorSelector = []
    divisorSize = bottomBar.width/(3*len(divisors))
    if divisorSize > buttonSize/2: divisorSize=buttonSize/2
    for i, d in enumerate(divisors):
        divisorSelector.append(Button(str(d), math.floor(i*divisorSize), math.floor((buttonSize/2-divisorSize)/2), math.ceil(divisorSize), math.ceil(divisorSize), (100, 100, 255), (0,0,0), onRelease=lambda x=d: selectDivisor(x), textSize = 30, scaler=1, hColor=hColor, textFont="Encode Sans"))
    selectDivisor(1)
    
    inBoxWidth = math.floor(bottomBar.width/3)-10
    inBoxHeight = math.floor(bottomBar.height/2)-6
    inBox = InputBox("", 5, 3, inBoxWidth, inBoxHeight, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor, textFont="Encode Sans")
    
    genMetronome()
    selectMetBeat(1)
    
    #adding to bottom bar
    bottomBar.addOption(ToolbarOption("scrollbar", scrollbar), Vector2(0,1))
    bottomBar.addOption(ToolbarOption("divisor", divisorSelector), Vector2(0,0))
    bottomBar.addOption(ToolbarOption("inBox", inBox), Vector2(1,0))
    bottomBar.addOption(ToolbarOption("metronome", metronome), Vector2(2,0))
    
    adjustTimingPointValues()

def hide():
    global selectedTile, lastTimingPoint, initailized
    gui.clear()
    songPlayer.unload()
    initailized = False
    selectedTile = None
    lastTimingPoint = None