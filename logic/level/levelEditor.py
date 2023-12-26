from ui.button import Button
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
from objects.tile import Tile
from logic.song.timingPoints import TimingPoint, TimeSignature
import logic.song.songPlayer as songPlayer
import graphics.gui as gui

def addOption(option, func, i):
    global toolbarButtons
    toolbarButtons.append(Button(option, toolbarPos.x + i*buttonSize, toolbarPos.y, buttonSize, buttonSize, (0, 255, 0), (255, 0, 0), func))

def select(option):
    global selected
    selected = option
    toolbarButtons[selected].color = (255, 0, 0)

def checkInput():
    global playing
    if input.keyBindings["play"].justPressed:
        if playing:
            songPlayer.pause()
            playing = False
        else:
            songPlayer.unpause()
            playing = True

def update():
    checkInput()
    print(getGridPos(Vector2(input.mousePos.x, input.mousePos.y)))
    for button in toolbarButtons:
        button.update()
    level.draw(gui.screen, songPlayer.getPos())
    
    global lastMousePos
    if selected == "move" and input.mouseBindings["lmb"].down:
        currentMousePos = Vector2(input.mousePos.x, input.mousePos.y)
        level.move(currentMousePos - lastMousePos)
        lastMousePos = currentMousePos
    else:
        lastMousePos = Vector2(input.mousePos.x, input.mousePos.y)
        
    if selected == "select" and input.mouseBindings["lmb"].justPressed:
        for tile in level.tiles:
            if tile.isOver(input.mousePos):
                global selectedTile
                selectedTile = getGridPos(tile.pos)
                break
    
    if selected == "platform" and input.mouseBindings["lmb"].justPressed:
        level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "platform"))
    
    if selected == "wall" and input.mouseBindings["lmb"].justPressed:
        level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "wall"))
        
    if selected == "rest" and input.mouseBindings["lmb"].justPressed:
        level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "rest"))
    
def draw():
    level.draw(gui.screen, songPlayer.getPos(), False, True)
    for button in toolbarButtons:
        button.draw(gui.screen)

def show():
    for i, option in enumerate(toolbarOptions):
        addOption(option, lambda x=option: select(x), i)

    global tiles, level
    songPlayer.load(r"Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))])
    
    tiles = [
        Tile(Vector2(0, 0), None, 0, songPlayer.getBeatByIndex(0, 1), "platform"),
        Tile(Vector2(0, 1), None, songPlayer.getBeatByIndex(0, 1), songPlayer.getBeatByIndex(1, 1), "platform"),
        Tile(Vector2(0, 2), None, songPlayer.getBeatByIndex(1, 1), songPlayer.getBeatByIndex(2, 1), "platform"),
        Tile(Vector2(1, 2), None, songPlayer.getBeatByIndex(2, 1), songPlayer.getBeatByIndex(3, 1), "platform"),
        Tile(Vector2(2, 2), None, songPlayer.getBeatByIndex(3, 1), songPlayer.getBeatByIndex(4, 1), "platform"),
    ]
    
    level = Level(tiles, 1, 1)
    
    global lastMousePos
    lastMousePos = Vector2(input.mousePos.x, input.mousePos.y)
    
    songPlayer.play()
    global playing
    playing = True
    update()

def load(level):
    pass

def getGridPos(pos):
    return (getRelGridPos(pos) - getRelGridPos(level.pos)).floor()

def getRelGridPos(pos):
    return Vector2(pos.x/level.tileSize.x, pos.y/level.tileSize.y)

toolbarOptions = ["move", "select", "platform", "wall", "rest", "save", "load"]
toolbarButtons = []
toolbarPos = Vector2(0, 0)
buttonSize = 50
selected = "move"
playing = False