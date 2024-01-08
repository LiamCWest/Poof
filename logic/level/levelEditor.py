from objects.tile import Tile
from ui.button import Button
from ui.toolbar import Toolbar, ToolbarOption
from ui.inputBox import InputBox
from ui.text import Text
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
import logic.song.songPlayer as songPlayer
import logic.song.timingPoints as timingPoints
from logic.song.timingPoints import TimingPoint, TimeSignature
import graphics.gui as gui
from utils.polygon import Polygon
from ui.scrollbar import Scrollbar
import bisect
import pygame

hColor = (150, 150, 255)

def updateFactors(factor):
    level.factor = factor

def selectMode(option):
    global selectedMode
    topBar.objects[modes.index(selectedMode)].baseObj.color = (100, 100, 255)
    selectedMode = option
    topBar.objects[modes.index(selectedMode)].baseObj.color = (50, 50, 255)

def selectDivisor(d):
    global divisor
    divisorSelector[divisors.index(divisor)].color = (100, 100, 255)
    divisor = d
    divisorSelector[divisors.index(d)].color = (50, 50, 255)

selectedTile = None
def checkInput():
    global level, divisor, selectedTile
    if input.keyActionBindings["play"].justPressed:
        if songPlayer.getIsPlaying():
            songPlayer.pause()
            songPlayer.seek(timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor))
        else:
            songPlayer.unpause()
       
    if input.specialKeyBindings["escape"].justPressed:
        gui.setScreen("main")
       
    if selectedTile:
        if input.keyActionBindings["moveTileLeft"].justPressed:
            selectedTile.pos += Vector2(-1, 0)
        if input.keyActionBindings["moveTileRight"].justPressed:
            selectedTile.pos += Vector2(1, 0)
        if input.keyActionBindings["moveTileUp"].justPressed:
            selectedTile.pos += Vector2(0, -1)
        if input.keyActionBindings["moveTileDown"].justPressed:
            selectedTile.pos += Vector2(0, 1)
        
        if input.keyActionBindings["increaseTileLength"].justPressed:
            newTileEndTime = timingPoints.getNextBeat(level.timingPoints, selectedTile.disappearTime, divisor)
            newTile = selectedTile.copy()
            newTile.disappearTime = newTileEndTime
            if level.isTileValid(newTile, selectedTile):
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile = newTile.copy()
                level.addTile(selectedTile)
        if input.keyActionBindings["decreaseTileLength"].justPressed:
            newTileEndTime = timingPoints.getPreviousBeat(level.timingPoints, selectedTile.disappearTime, divisor)
            if newTileEndTime >= selectedTile.appearedTime:
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile.disappearTime = newTileEndTime
                level.addTile(selectedTile)

    if input.keyActionBindings["timeForwards"].justPressed:
        oldTime = songPlayer.getPos()
        songPlayer.seek(min(timingPoints.getNextBeat(level.timingPoints, oldTime, divisor), songPlayer.getSongLength()))
        delta = songPlayer.getPos() - oldTime
        if selectedTile:
            newTile = selectedTile.copy()
            newTile.appearedTime += delta
            newTile.disappearTime += delta
            if level.isTileValid(newTile, selectedTile):
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile = newTile.copy()
                level.addTile(selectedTile)
        
    if input.keyActionBindings["timeBackwards"].justPressed:
        oldTime = songPlayer.getPos()
        songPlayer.seek(max(0, timingPoints.getPreviousBeat(level.timingPoints, oldTime, divisor)))
        delta = songPlayer.getPos() - oldTime
        if selectedTile:
            newTile = selectedTile.copy()
            newTile.appearedTime += delta
            newTile.disappearTime += delta
            if level.isTileValid(newTile, selectedTile):
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile = newTile.copy()
                level.addTile(selectedTile)

levelPos = Vector2(0, 0)
def update():
    checkInput()
    metronomeUpdate()
    timingPointUpdate()
    topBar.update()
    bottomBar.update()
    
    global lastScrollbarValue, divisor
    songLen = songPlayer.getSongLength()
    if scrollbar.getValue() != lastScrollbarValue: 
        songPos = songLen * scrollbar.getValue()
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
        
        if selectedMode in ["platform", "wall", "rest"] and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor)
            if level.getTileAt(tilePos, tileTime) is None:
                level.addTile(Tile(tilePos, None, tileTime, tileTime, selectedMode))
                selectedTile = level.getTileAt(tilePos, tileTime)
                selectedTile.factor = level.factor
            
        if selectedMode == "delete" and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = timingPoints.getNearestBeat(level.timingPoints, songPlayer.getPos(), divisor)
            level.removeTileAt(tilePos, tileTime)
            selectedTile = None

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
        metronome.append(Polygon.fromRect((i*metronomeSize, 0, metronomeSize, metronomeSize), (100, 100, 255)))
    metronome.append(Text("1", metronomeSize/2, metronomeSize/2, (0,0,0), 30, width=metronomeSize, height=metronomeSize))
    if bottomBar.grid[0][2]:
        bottomBar.grid[0][2].baseObj = metronome

def deletePoint():
    global level
    prevPoint = timingPoints.getPreviousPoint(level.timingPoints, songPlayer.getPos())
    point = prevPoint if prevPoint else level.timingPoints[0]
    level.timingPoints.remove(point)

initailized = False
def init():
    global topBar, bottomBar, modes, divisorSelector, divisors, scrollbar, selectedMode, divisor, initailized, lastScrollbarValue, metronome, metronomeSize, buttonSize, bpm, timeSig
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

    modes = ["move", "select", "platform", "wall", "rest", "delete"] # possible modes
    topbarButtons = { # buttons on the top bar
        "save": lambda: level.save(levelF), 
        "load": lambda: loadLevel("level_data.json"),
        "delete\npoint": lambda: deletePoint(),
    }
    bpmText = Text("BPM", buttonSize/2, buttonSize/4, (0,0,0), fontSize, bgColor=(100, 100, 255), width = buttonSize, height = buttonSize/2) # text for bpm
    bpmBox = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor) # input box for bpm
    bpm = [bpmText, bpmBox] # bpm text and input box
    timeSigNum = InputBox("", 0, 0, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor) # input box for time signature numerator
    timeSigDenom = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1, clearOnInput=False, numOnly=True, hColor=hColor) # input box for time signature denominator
    timeSig = [timeSigNum, timeSigDenom] # time signature numerator and denominator

    # fuction to create buttons for the toolbar, could probably be moved somewhere else. ToolbarOption.fromButton?
    barButton = lambda option, func: Button(
        option, 0, 0, buttonSize, buttonSize, (100, 100, 255), 
        (0, 0, 0), func, textSize = fontSize, scaler=1, hColor=hColor
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
    print(buttonSize, divisorSize, buttonSize-divisorSize)
    for i, d in enumerate(divisors):
        divisorSelector.append(Button(str(d), i*divisorSize, (buttonSize/2-divisorSize)/2, divisorSize, divisorSize, (100, 100, 255), (0,0,0), lambda x=d: selectDivisor(x), textSize = 30, scaler=1, hColor=hColor))
    selectDivisor(1)
        
    genMetronome()
    selectMetBeat(1)
    
    #adding to bottom bar
    bottomBar.addOption(ToolbarOption("scrollbar", scrollbar), Vector2(0,1))
    bottomBar.addOption(ToolbarOption("divisor", divisorSelector), Vector2(0,0))
    bottomBar.addOption(ToolbarOption("metronome", metronome), Vector2(2,0))
    
    adjustTimingPointValues()
    
def hide():
    gui.clear()
    songPlayer.unload()
    initailized = False
    global selectedTile, lastTimingPoint
    selectedTile = None
    lastTimingPoint = None