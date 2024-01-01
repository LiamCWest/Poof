from objects.tile import Tile
from ui.button import Button
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
import logic.song.songPlayer as songPlayer
import graphics.gui as gui
from utils.polygon import Polygon
from ui.scrollbar import Scrollbar
from logic.song.timingPoints import TimingPoint, TimeSignature, getNextBeat
import json
import hashlib

def addOption(option, func, i):
    global toolbarButtons
    toolbarButtons.append(Button(option, toolbarPos.x + buttonSize*0.1 + i*(buttonSize*1.1), toolbarPos.y + buttonSize*0.1, buttonSize, buttonSize, (100, 100, 255), (0, 0, 0), func, textSize = 15, scaler=1.1))

selected = None
def select(option):
    global selected
    toolbarButtons[toolbarModes.index(selected)].color = (100, 100, 255)
    selected = option
    toolbarButtons[toolbarModes.index(selected)].color = (50, 50, 255)

def checkInput():
    global level
    if input.keyBindings["play"].justPressed:
        if songPlayer.getIsPlaying():
            songPlayer.pause()
        else:
            songPlayer.unpause()
       
    if "selectedTile" in globals() and selectedTile:    
        if input.keyBindings["moveTileLeft"].justPressed:
            moveTile(selectedTile, Vector2(-1, 0))
        if input.keyBindings["moveTileRight"].justPressed:
            moveTile(selectedTile, Vector2(1, 0))
        if input.keyBindings["moveTileUp"].justPressed:
            moveTile(selectedTile, Vector2(0, -1))
        if input.keyBindings["moveTileDown"].justPressed:
            moveTile(selectedTile, Vector2(0, 1))

def moveTile(pos, delta):
    global level, selectedTile
    tile = level.getTileByPos(pos)
    tile.pos += delta
    selectedTile += delta

levelPos = Vector2(0, 0)
def update():
    checkInput()
    for button in toolbarButtons:
        button.update()
    global lastScrollbarValue
    scrollbar.update()
    songLen = songPlayer.getSongLength()
    
    if scrollbar.getValue() != lastScrollbarValue: songPlayer.seek(songLen * scrollbar.getValue())
    else: scrollbar.moveTo(songPlayer.getPos() / songLen)
    lastScrollbarValue = scrollbar.getValue()

    if not posIn(input.mousePos.pos, (toolbarPos.x, toolbarPos.y, toolbar.getWidth(), toolbar.getHeight())):
        global lastMousePos, levelPos
        if selected == "move" and input.mouseBindings["lmb"].pressed:
            currentMousePos = input.mousePos.pos
            levelPos -= (currentMousePos - lastMousePos) / level.tileSize
            lastMousePos = currentMousePos
        else:
            lastMousePos = input.mousePos.pos
            
        if selected == "select" and input.mouseBindings["lmb"].justPressed:
            global selectedTile
            tilePos = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            if "selectedTile" in globals() and selectedTile and tilePos == selectedTile:
                    selectedTile = None
            else:
                selectedTile = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
        
        if selected in ["platform", "wall", "rest"] and input.mouseBindings["lmb"].down:
            nextBeat = getNextBeat(songPlayer.currentTimingPoints,songPlayer.getPos(), 1)
            level.addTile(Tile(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), None, nextBeat, nextBeat, selected))
            selectedTile = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
            
        if selected == "delete" and input.mouseBindings["lmb"].justPressed:
            tile = level.getTileByPos(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos))
            if tile is not None:
                level.removeTile(tile)
                selectedTile = None

def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    global levelPos
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, drawGrid=True)
    toolbar.draw(gui.screen)
    for button in toolbarButtons:
        button.draw(gui.screen)
    scrollbar.draw(gui.screen)

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

    songPlayer.load(r"Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))]) #Temp
    
    tiles = [
        Tile(Vector2(0, 0), None, 0, songPlayer.getBeatByIndex(0, 1), "platform"),
        Tile(Vector2(0, 1), None, songPlayer.getBeatByIndex(0, 1), songPlayer.getBeatByIndex(1, 1), "platform"),
        Tile(Vector2(0, 2), None, songPlayer.getBeatByIndex(1, 1), songPlayer.getBeatByIndex(2, 1), "platform"),
        Tile(Vector2(1, 2), None, songPlayer.getBeatByIndex(2, 1), songPlayer.getBeatByIndex(3, 1), "platform"),
        Tile(Vector2(2, 2), None, songPlayer.getBeatByIndex(3, 1), songPlayer.getBeatByIndex(4, 1), "platform"),
    ]
    songPlayer.unload() #Temp
    
    level = Level(tiles, 1, 1, "Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))], Vector2(0, 0), 0)
    
    lastMousePos = input.mousePos.pos
    
    update()

def getLevel(levelFile):
    global levelF
    levelF = levelFile
    with open(levelFile, 'r') as file:
        saved_data = json.load(file)
        loaded_data = saved_data['data']
        saved_signature = saved_data['signature']
        if not checkSignature(loaded_data, saved_signature):
            print("Level file corrupted")
            return None
        tiles = loaded_data['tiles']
        tilesV2 = [Tile(Vector2.from_tuple(tile[0]), tile[1], tile[2], tile[3], tile[4]) for tile in tiles]
        appearLength = loaded_data['appearLength']
        disappearLength = loaded_data['disappearLength']
        songPath = loaded_data['songPath']
        timingPointsVals = loaded_data['timingPoints']
        timingPoints = [TimingPoint(timingPoint[0], timingPoint[1], TimeSignature(timingPoint[2], timingPoint[3])) for timingPoint in timingPointsVals]
        playerStartPos = Vector2.from_tuple(loaded_data['playerStartPos'])
        playerStartTime = loaded_data['playerStartTime']
        level = Level(tilesV2, appearLength, disappearLength, songPath, timingPoints, playerStartPos, playerStartTime)
        return level
    
def loadLevel(levelFile):
    global level
    songPlayer.unload()
    level = getLevel(levelFile)

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
scrollbar = Scrollbar(toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + buttonSize*0.1, toolbarPos.y+buttonSize*1.2/2-5, 10, 100, "h", sliderWidth=25)
toolbar = Polygon.fromRect((toolbarPos.x, toolbarPos.y, len(toolbarOptions)*(buttonSize*1.1) + buttonSize*0.2 + scrollbar.length, buttonSize*1.2), (25, 25, 100))
lastScrollbarValue = 0