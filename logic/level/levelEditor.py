from ui.button import Button
from utils.vector2 import Vector2
import input.input as input
from logic.level.level import Level
from objects.tile import Tile
from logic.song.timingPoints import TimingPoint, TimeSignature
import logic.song.songPlayer as songPlayer
import graphics.gui as gui
from utils.polygon import Polygon
from ui.scrollbar import Scrollbar

def addOption(option, func, i):
    global toolbarButtons
    toolbarButtons.append(Button(option, toolbarPos.x + i*(buttonSize*1.1), toolbarPos.y, buttonSize, buttonSize, (100, 100, 255), (0, 0, 0), func, textSize = 15, scaler=1.1))

def select(option):
    global selected
    toolbarButtons[toolbarOptions.index(selected)].color = (100, 100, 255)
    selected = option
    toolbarButtons[toolbarOptions.index(selected)].color = (50, 50, 255)

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
    for button in toolbarButtons:
        button.update()
    global lastPercent
    scrollbar.update()
    songLen = 10 #songPlayer.getSongLength()
    # if scrollbar.perc != lastPercent: 
    songPlayer.seek(songLen * scrollbar.perc)
    # else: scrollbar.move(songPlayer.getPos()/songLen)
    lastPercent = scrollbar.perc
    
    level.draw(gui.screen, songPlayer.getPos())
    if not posIn(input.mousePos, (toolbarPos.x, toolbarPos.y, len(toolbarOptions)*(buttonSize*1.1) +100, buttonSize*1.1)):
        global lastMousePos
        if selected == "move" and input.mouseBindings["lmb"].down:
            currentMousePos = Vector2(input.mousePos.x, input.mousePos.y)
            level.move(currentMousePos - lastMousePos)
            lastMousePos = currentMousePos
        else:
            lastMousePos = Vector2(input.mousePos.x, input.mousePos.y)
            
        if selected == "select" and input.mouseBindings["lmb"].justPressed:
            global selectedTile
            selectedTile = getGridPos(input.mousePos)
        
        if selected == "platform" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getPos(), songPlayer.getPos(), "platform"))
        
        if selected == "wall" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getPos(), songPlayer.getPos(), "wall"))
            
        if selected == "rest" and input.mouseBindings["lmb"].justPressed:
            level.addTile(Tile(getGridPos(input.mousePos), None, songPlayer.getPos(), songPlayer.getPos(), "rest"))
    
def posIn(pos, rect):
    return pos.x > rect[0] and pos.x < rect[0] + rect[2] and pos.y > rect[1] and pos.y < rect[1] + rect[3]
    
def draw():
    level.draw(gui.screen, songPlayer.getPos(), False, True)
    toolbar.draw(gui.screen)
    for button in toolbarButtons:
        button.draw(gui.screen)
    scrollbar.draw(gui.screen)

def show():
    for i, option in enumerate(toolbarOptions):
        addOption(option, lambda x=option: select(x), i)
    select("move")

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
buttonSize = 55
toolbarPos = Vector2(buttonSize*0.1, buttonSize*0.1)
selected = "move"
playing = False
toolbar = Polygon([(toolbarPos.x, toolbarPos.y), 
                   (toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + 100, toolbarPos.y), 
                   (toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1) + 100, toolbarPos.y + buttonSize*1.1), 
                   (toolbarPos.x, toolbarPos.y + buttonSize*1.1)], (25, 25, 100))
scrollbar = Scrollbar(toolbarPos.x + len(toolbarOptions)*(buttonSize*1.1), toolbarPos.y+buttonSize/2-10, 20, 100, "h", [i for i in range(100)], 20)
lastPercent = 0