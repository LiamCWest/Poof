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

def update():
    for button in toolbarButtons:
        button.update()
    level.update(gui.screen, songPlayer.getTime())
    
    if selected == "move" and input.mouseBindings["lmb"].down:
        global lastMousePos
        currentMousePos = input.mousePos
        level.move(currentMousePos - lastMousePos)
        lastMousePos = currentMousePos
        
    if selected == "select" and input.mouseBindings["lmb"].justPressed:
        for tile in level.tiles:
            if tile.isOver(input.mousePos):
                global selectedTile
                selectedTile = getGridPos(tile.pos)
                break
    
    if selected == "platform" and input.mouseBindings["lmb"].justPressed:
        level.tiles.append(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "platform"))
    
    if selected == "wall" and input.mouseBindings["lmb"].justPressed:
        level.tiles.append(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "wall"))
        
    if selected == "rest" and input.mouseBindings["lmb"].justPressed:
        level.tiles.append(Tile(getGridPos(input.mousePos), None, songPlayer.getTime(), songPlayer.getTime() + 1, "rest"))
    
def draw():
    for button in toolbarButtons:
        button.draw()

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
    
    songPlayer.play()
    update()

def load(level):
    pass

def getGridPos(tilePos):
    pass

toolbarOptions = ["move", "select", "platform", "wall", "rest", "save", "load"]
toolbarButtons = []
toolbarPos = Vector2(0, 0)
buttonSize = 50