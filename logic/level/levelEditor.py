from objects.tile import Tile
from ui.button import Button
from ui.toolbar import Toolbar, ToolbarOption
from ui.inputBox import InputBox
from ui.text import Text
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
import logic.song.songPlayer as songPlayer
import graphics.gui as gui
from utils.polygon import Polygon
from ui.scrollbar import Scrollbar
import pygame
import json
import hashlib
import math

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
            songPlayer.seek(songPlayer.getNearestBeat(divisor))
        else:
            songPlayer.unpause()
       
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
            newTileEndTime = songPlayer.getNextBeat(divisor, selectedTile.disappearTime)
            newTile = selectedTile.copy()
            newTile.disappearTime = newTileEndTime
            if level.isTileValid(newTile, selectedTile):
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile = newTile.copy()
                level.addTile(selectedTile)
        if input.keyActionBindings["decreaseTileLength"].justPressed:
            newTileEndTime = songPlayer.getPreviousBeat(divisor, selectedTile.disappearTime)
            if newTileEndTime >= selectedTile.appearedTime:
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile.disappearTime = newTileEndTime
                level.addTile(selectedTile)

    if input.keyActionBindings["timeForwards"].justPressed:
        oldTime = songPlayer.getPos()
        songPlayer.seek(songPlayer.getNextBeat(divisor))
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
        songPlayer.seek(max(0, songPlayer.getPreviousBeat(divisor)))
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
    topBar.update()
    bottomBar.update()
    
    global lastScrollbarValue, divisor
    songLen = songPlayer.getSongLength()
    if scrollbar.getValue() != lastScrollbarValue: 
        songPos = songLen * scrollbar.getValue()
        roundedSongPos = songPlayer.getNearestBeat(divisor, songPos)
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
            tileTime = songPlayer.getNearestBeat(divisor, songPlayer.getPos())
            if level.getTileAt(tilePos, tileTime) is None:
                level.addTile(Tile(tilePos, None, tileTime, tileTime, selectedMode))
                selectedTile = level.getTileAt(tilePos, tileTime)
                selectedTile.factor = level.factor
            
        if selectedMode == "delete" and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = songPlayer.getNearestBeat(divisor, songPlayer.getPos())
            level.removeTileAt(tilePos, tileTime)
            selectedTile = None

def metronomeUpdate(): #TODO: make beat number apear on each beat
    point = songPlayer.getPreviousPoint() if songPlayer.getPreviousPoint() else songPlayer.currentTimingPoints[0]
    if len(metronome) != point.timeSignature.num + 1:
        genMetronome()
    distanceFromPoint = songPlayer.getPos() - point.time if songPlayer.getPos() > point.time else None
    b = 1 if distanceFromPoint is None else math.floor(distanceFromPoint / point.beatLength) % point.timeSignature.num + 1
    selectMetBeat(b)
            
def selectMetBeat(b):
    global beat, metronome
    metronome[beat-1].color = (100, 100, 255)
    beat = b
    metronome[b-1].color = (50, 50, 255) if beat != 1 else (0, 150, 200)
    metronome[-1].text = str(beat)
    metronome[-1].x = metronome[b-1].pos.x
def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    global levelPos, selectedTile
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, drawGrid=True)
    topBar.draw(gui.screen)
    bottomBar.draw(gui.screen)
    
    if selectedTile and selectedTile.appearedTime-level.appearLength <= songPlayer.getPos() <= selectedTile.disappearTime+level.disappearLength:
        s = pygame.Surface(level.tileSize.toTuple())
        s.set_alpha(128)
        s.fill((255,255,255))
        gui.screen.blit(s, ((selectedTile.pos - levelPos) * level.tileSize).toTuple())
    elif selectedTile:
        selectedTile = None
        
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

def checkSignature(data, signature):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest() == signature

def genMetronome():
    global metronome, metronomeSize, beat
    prevPoint = songPlayer.getPreviousPoint()
    prevPoint = prevPoint if prevPoint else songPlayer.currentTimingPoints[0]
    metronomeLen = prevPoint.timeSignature.num # length of a measure
    metronome = []
    metronomeSize = bottomBar.width/(3*metronomeLen)
    if metronomeSize > buttonSize/2: metronomeSize = buttonSize/2
    for i in range(metronomeLen):
        metronome.append(Polygon.fromRect((i*metronomeSize, 0, metronomeSize, metronomeSize), (100, 100, 255)))
    metronome.append(Text(str(beat), metronomeSize/2, metronomeSize/2, (0,0,0), 30, width=metronomeSize, height=metronomeSize, bgColor=(0, 150, 200)))

initailized = False
def init():
    global topBar, bottomBar, modes, divisorSelector, divisors, scrollbar, selectedMode, divisor, initailized, lastScrollbarValue, beat, metronome, metronomeSize, buttonSize
    if initailized: return
    initailized = True
    # vars
    buttonSize = 90
    lastScrollbarValue = 0
    fontSize = 20

    # top bar #
    w = buttonSize*10 # width of the top bar
    topBar = Toolbar(Vector2(10, 1), Vector2((gui.screen.get_width()-w)//2, 0), w, buttonSize) # toolbar for the top bar

    modes = ["move", "select", "platform", "wall", "rest", "delete"] # possible modes
    topbarButtons = { # buttons on the top bar
        "save": lambda: level.save(levelF), 
        "load": lambda: loadLevel("level_data.json")
    }
    bpmText = Text("BPM", buttonSize/2, buttonSize/4, (0,0,0), fontSize, bgColor=(100, 100, 255), width = buttonSize, height = buttonSize/2) # text for bpm
    bpmBox = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1) # input box for bpm
    bpm = [bpmText, bpmBox] # bpm text and input box
    timeSigNum = InputBox("", 0, 0, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1) # input box for time signature numerator
    timeSigDenom = InputBox("", 0, buttonSize/2, buttonSize, buttonSize/2, (100, 100, 255), (0, 0, 0), fontSize, True, scaler=1) # input box for time signature denominator
    timeSig = [timeSigNum, timeSigDenom] # time signature numerator and denominator

    # fuction to create buttons for the toolbar, could probably be moved somewhere else. ToolbarOption.fromButton?
    barButton = lambda option, func: Button(
        option, 0, 0, buttonSize, buttonSize, (100, 100, 255), 
        (0, 0, 0), func, textSize = fontSize, scaler=1.1
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
    divisors = [1, 2, 4, 8, 16]
    divisorSelector = []
    divisorSize = bottomBar.width/(3*len(divisors))
    if divisorSize > buttonSize/2: divisorSize=buttonSize/2
    for i, d in enumerate(divisors):
        divisorSelector.append(Button(str(d), i*divisorSize, 0, divisorSize, divisorSize, (100, 100, 255), (0,0,0), lambda x=d: selectDivisor(x), textSize = 30, scaler=1.1))
    selectDivisor(1)
        
    beat = 1
    genMetronome()
    selectMetBeat(1)
    
    #adding to bottom bar
    bottomBar.addOption(ToolbarOption("scrollbar", scrollbar), Vector2(0,1))
    bottomBar.addOption(ToolbarOption("divisor", divisorSelector), Vector2(0,0))
    bottomBar.addOption(ToolbarOption("metronome", metronome), Vector2(2,0))