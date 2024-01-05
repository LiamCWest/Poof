from objects.tile import Tile
from ui.button import Button
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

def addOption(option, func, i):
    global toolbarButtons
    toolbarButtons.append(Button(option, toolbarPos.x + buttonSize*0.1 + i*(buttonSize*1.1), toolbarPos.y + buttonSize*0.1, buttonSize, buttonSize, (100, 100, 255), (0, 0, 0), func, textSize = 15, scaler=1.1))

def updateFactors(factor):
    level.factor = factor

selected = None
def select(option):
    global selected
    toolbarButtons[toolbarModes.index(selected)].color = (100, 100, 255)
    selected = option
    toolbarButtons[toolbarModes.index(selected)].color = (50, 50, 255)

def selectDivisor(d):
    global divisor
    divisorSelector[divisors.index(divisor)].color = (100, 100, 255)
    divisor = d
    divisorSelector[divisors.index(d)].color = (50, 50, 255)

selectedTile = None
def checkInput():
    global level, divisor, selectedTile
    if input.keyBindings["play"].justPressed:
        if songPlayer.getIsPlaying():
            songPlayer.pause()
            songPlayer.seek(songPlayer.getNearestBeat(divisor))
        else:
            songPlayer.unpause()
       
    if selectedTile:
        if input.keyBindings["moveTileLeft"].justPressed and not input.modifierBindings["shift"].pressed:
            selectedTile.pos += Vector2(-1, 0)
        if input.keyBindings["moveTileRight"].justPressed and not input.modifierBindings["shift"].pressed:
            selectedTile.pos += Vector2(1, 0)
        if input.keyBindings["moveTileUp"].justPressed and not input.modifierBindings["shift"].pressed:
            selectedTile.pos += Vector2(0, -1)
        if input.keyBindings["moveTileDown"].justPressed and not input.modifierBindings["shift"].pressed:
            selectedTile.pos += Vector2(0, 1)
        
        if input.keyBindings["increaseTileLength"].justPressed:
            newTileEndTime = songPlayer.getNextBeat(divisor, selectedTile.disappearTime)
            newTile = selectedTile.copy()
            newTile.disappearTime = newTileEndTime
            if level.isTileValid(newTile, selectedTile):
                print("valid")
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile = newTile.copy()
                level.addTile(selectedTile)
        if input.keyBindings["decreaseTileLength"].justPressed:
            newTileEndTime = songPlayer.getPreviousBeat(divisor, selectedTile.disappearTime)
            if newTileEndTime >= selectedTile.appearedTime:
                level.removeTileAt(selectedTile.pos, selectedTile.appearedTime)
                selectedTile.disappearTime = newTileEndTime
                level.addTile(selectedTile)

    if input.keyBindings["timeForwards"].justPressed:
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
        
    if input.keyBindings["timeBackwards"].justPressed:
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
    for button in toolbarButtons:
        button.update()
    for button in divisorSelector:
        button.update()
    
    global lastScrollbarValue, divisor
    scrollbar.update()
    songLen = songPlayer.getSongLength()
    if scrollbar.getValue() != lastScrollbarValue: 
        songPos = songLen * scrollbar.getValue()
        roundedSongPos = songPlayer.getNearestBeat(divisor, songPos)
        songPlayer.seek(roundedSongPos)
        scrollbar.moveTo(roundedSongPos / songLen)
    else: 
        scrollbar.moveTo(songPlayer.getPos() / songLen)
    lastScrollbarValue = scrollbar.getValue()

    if not posIn(input.mousePos.pos, (toolbarPos.x, toolbarPos.y, toolbar.getWidth(), toolbar.getHeight())):
        global lastMousePos, levelPos, selectedTile
        if selected == "move" and input.mouseBindings["lmb"].pressed:
            currentMousePos = input.mousePos.pos
            levelPos -= (currentMousePos - lastMousePos) / level.tileSize
            lastMousePos = currentMousePos
        else:
            lastMousePos = input.mousePos.pos
            
        if selected == "select" and input.mouseBindings["lmb"].justPressed:
            selectedTile = level.getTileAt(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), songPlayer.getPos())
        
        if selected in ["platform", "wall", "rest"] and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = songPlayer.getNearestBeat(divisor, songPlayer.getPos())
            if level.getTileAt(tilePos, tileTime) is None:
                level.addTile(Tile(tilePos, None, tileTime, tileTime, selected))
                selectedTile = level.getTileAt(tilePos, tileTime)
            
        if selected == "delete" and input.mouseBindings["lmb"].justPressed:
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            tileTime = songPlayer.getNearestBeat(divisor, songPlayer.getPos())
            level.removeTileAt(tilePos, tileTime)
            selectedTile = None

def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    global levelPos, selectedTile
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, drawGrid=True)
    toolbar.draw(gui.screen)
    for button in toolbarButtons:
        button.draw(gui.screen)
    scrollbar.draw(gui.screen)
    for button in divisorSelector:
        button.draw(gui.screen)
    
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
    global tiles, level, lastMousePos
    
    for i, option in enumerate(toolbarModes):
        addOption(option, lambda x=option: select(x), i)
    for option in toolbarB:
        i += 1
        addOption(option, toolbarFuncs[option], i)
    select("move")
    for i, d in enumerate(divisors):
        divisorSelector.append(Button(str(d), toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + buttonSize/2.75*0.1 + buttonSize/2.75*1.1*i, toolbarPos.y + buttonSize*1.2/4-5 + 20, buttonSize/2.75, buttonSize/2.75, (100, 100, 255), (0, 0, 0), lambda x=d: selectDivisor(x), textSize = 15, scaler=1.1))
    selectDivisor(1)
    lastMousePos = input.mousePos.pos
    
    update()
    
def loadLevel(levelFile):
    global level, levelF
    levelF = levelFile
    songPlayer.unload()
    level = Level.fromFile(levelFile)

def checkSignature(data, signature):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest() == signature

toolbarModes = ["move", "select", "platform", "wall", "rest", "delete"]
toolbarB = ["save", "load"]
toolbarOptions = toolbarModes + toolbarB
toolbarButtons = []
toolbarFuncs = {
    "save": lambda: level.save(levelF),
    "load": lambda: loadLevel("level_data.json")
}
buttonSize = 55
toolbarPos = Vector2(buttonSize*0.1, buttonSize*0.1)
selected = "move"
scrollbar = Scrollbar(toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + buttonSize*0.1, toolbarPos.y+buttonSize*1.2/4-5, 10, 100, "h", sliderWidth=25)
toolbar = Polygon.fromRect((toolbarPos.x, toolbarPos.y, len(toolbarOptions)*(buttonSize*1.1) + buttonSize*0.2 + scrollbar.length, buttonSize*1.2), (25, 25, 100))
divisors = [1, 2, 4, 8, 16]
divisorSelector = []
lastScrollbarValue = 0
divisor = 1