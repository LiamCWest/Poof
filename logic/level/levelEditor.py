from objects.tile import Tile
from ui.button import Button
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
import logic.song.songPlayer as songPlayer
import graphics.gui as gui
from utils.polygon import Polygon
from ui.scrollbar import Scrollbar
from logic.song.timingPoints import TimingPoint, TimeSignature
import json
import hashlib

def addOption(option, func, i):
    global toolbarButtons
    toolbarButtons.append(Button(option, toolbarPos.x + i*(buttonSize*1.1), toolbarPos.y, buttonSize, buttonSize, (100, 100, 255), (0, 0, 0), func, textSize = 15, scaler=1.1))

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

levelPos = Vector2(0, 0)
def update():
    checkInput()
    for button in toolbarButtons:
        button.update()
    global lastPercent
    scrollbar.update()
    songLen = songPlayer.getSongLength()
    if scrollbar.perc != lastPercent: songPlayer.seek(songLen * scrollbar.perc)
    else: scrollbar.move(songPlayer.getPos()/songLen)
    lastPercent = scrollbar.perc

    if not posIn(input.mousePos.pos, (toolbarPos.x, toolbarPos.y, len(toolbarOptions)*(buttonSize*1.1) +100, buttonSize*1.1)):
        global lastMousePos, levelPos
        if selected == "move" and input.mouseBindings["lmb"].down:
            currentMousePos = input.mousePos.pos
            levelPos += (currentMousePos - lastMousePos).divide(59)
            lastMousePos = currentMousePos
        else:
            lastMousePos = input.mousePos.pos
            
        if selected == "select" and input.mouseBindings["lmb"].justPressed:
            global selectedTile
            selectedTile = level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos)
        
        if selected == "platform" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), None, songPlayer.getPos(), songPlayer.getPos(), "platform"))
        
        if selected == "wall" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), None, songPlayer.getPos(), songPlayer.getPos(), "wall"))
            
        if selected == "rest" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(level.screenPosToRoundedTilePos(input.mousePos.pos, levelPos), None, songPlayer.getPos(), songPlayer.getPos(), "rest"))
    
def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    global levelPos
    level.draw(gui.screen, songPlayer.getPos(), levelPos, level.tileSize, False)
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

def loadLevel(levelFile):
    with open(levelFile, 'r') as file:
        saved_data = json.load(file)
        loaded_data = saved_data['data']
        saved_signature = saved_data['signature']
        if not checkSignature(loaded_data, saved_signature):
            print("Level file corrupted")
            return None
        tiles = loaded_data['tiles']
        tilesV2 = []
        for tile in tiles:
            tilesV2.append([Vector2.from_tuple(tile[0]), tile[1], tile[2], tile[3], tile[4]])
        appearLength = loaded_data['appearLength']
        disappearLength = loaded_data['disappearLength']
        songPath = loaded_data['songPath']
        level = Level(tilesV2, appearLength, disappearLength, songPath)
        print("Level loaded:", tilesV2, appearLength, disappearLength, songPath)
        return level

def checkSignature(data, signature):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest() == signature

def getGridPos(pos):
    return (getRelGridPos(pos) - getRelGridPos(level.pos)).floor()

def getRelGridPos(pos):
    return Vector2(pos.x/level.tileSize.x, pos.y/level.tileSize.y)

toolbarModes = ["move", "select", "platform", "wall", "rest"]
toolbarB = ["save", "load"]
toolbarOptions = toolbarModes + toolbarB
toolbarButtons = []
toolbarFuncs = {
    "save": lambda: level.save(),
    "load": lambda: loadLevel("level_data.json")
}
buttonSize = 55
toolbarPos = Vector2(buttonSize*0.1, buttonSize*0.1)
selected = "move"
toolbar = Polygon([(toolbarPos.x, toolbarPos.y), 
                   (toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + 100, toolbarPos.y), 
                   (toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + 100, toolbarPos.y + buttonSize*1.1), 
                   (toolbarPos.x, toolbarPos.y + buttonSize*1.1)], (25, 25, 100))
scrollbar = Scrollbar(toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1), toolbarPos.y+buttonSize/2-10, 20, 100, "h", [i for i in range(100)], 20)
lastPercent = 0