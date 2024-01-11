import os

from graphics import gui
from ui.button import Button
from ui.popup import Popup
from ui.inputBox import InputBox
from ui.text import Text
from utils.vector2 import Vector2
from logic.level.level import Level
from logic.song.timingPoints import TimeSignature, TimingPoint
from objects.tile import Tile
from graphics.particleSystem.shapedEmitter import ShapedEmitter

popups = []
def show():
    global levels, buttons, popupOpen, popups
    if isLE: buttons.append(Button("New Level", gui.screen.get_width()/2-150, 500, 300, 50, (255,0,0), (0,0,0), newLevel))
    else: buttons = []
    levels = getLevels("levels")
    levelButtons = []
    for i, level in enumerate(levels):
        levelButtons.append(genLevelButton(level, i))
    buttons += levelButtons
    
    popupOpen = False
    nLW = 500
    genericParticles = ShapedEmitter(None, None, Vector2(2,2), 250, 15, 5)
    popups = {
        "newLevel": Popup(Vector2((1280-nLW)/2, 0), nLW, 650, (0,0,0), None,
                        [
                            InputBox("Level Name", (nLW-400)/2, 150, 400, 50, (80, 93, 112), (255,255,255), 30, scaler = 1.1),
                            InputBox("Song File", (nLW-400)/2, 225, 400, 50, (80, 93, 112), (255,255,255), 30, scaler = 1.1),
                            InputBox("Offset", (nLW-400)/2, 325, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1),
                            InputBox("BPM", (nLW-400)/2, 375, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1),
                            InputBox("Num", (nLW)/2 + 25, 325, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1),
                            InputBox("Denom", (nLW)/2 + 25, 375, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1),
                            Button("Create", (nLW-400)/2, 475, 400, 50, (80, 93, 112), (255,255,255), createLevel, particles = genericParticles, particlesOnOver = True, scaler = 1.1),
                            Button("Close", (nLW-400)/2, 550, 400, 50, (80, 93, 112), (255,255,255), popupClose, scaler = 1.1),
                         ],
                        [Text("New Level", nLW/2, 75, (255, 255, 255), 60, fontPath = "ROGFONTS-REGULAR.ttf")]),
    }

isLE = False
def start(load, isLevelEditor = False):
    global loadLevel, isLE
    loadLevel = load
    isLE = isLevelEditor

def hide():
    pass

def update():
    global buttons, popups, popupOpen
    if not popupOpen:
        for button in buttons:
            button.update()
    for popup in popups.values():
        popup.update()

def draw():
    global buttons, popups
    for button in buttons:
        button.draw(gui.screen)
    for popup in popups.values():
        popup.draw()

def genLevelButton(level, i):
    rowLength = 5
    x = 100 + (i % rowLength) * 200
    y = 100 + (i // rowLength) * 150
    return Button(getLevelName(level), x, y, 200, 200, (0,0,0), (255,255,255), lambda: loadLevel(level))

def newLevel():
    global popups, popupOpen
    popupOpen = True
    popups["newLevel"].show()

def createLevel():
    global popups, popupOpen
    levelPopup = popups["newLevel"]
    if any([inputBox.output != "" for inputBox in levelPopup.objects[:2]]):
        levelName = levelPopup.objects[0].output
        song = levelPopup.objects[1].output
        offset = float(levelPopup.objects[2].output)
        bpm = int(levelPopup.objects[3].output)
        num = int(levelPopup.objects[4].output)
        denom = int(levelPopup.objects[5].output)
        timeSig = TimeSignature(num, denom)
        timingPoint = TimingPoint(offset, bpm, timeSig)
        
        nLevel = Level([Tile(Vector2(0, 0), None, 0, offset, "platform")], 1, 1, song, [timingPoint], Vector2(0,0), 0)
        nLevel.save("levels/" + levelName + ".json")
    
def popupClose():
    global popups, popupOpen
    popupOpen = False
    for popup in popups.values():
        if popup.open: popup.hide()

def getLevelName(level):
    return os.path.basename(level).split(".")[0]

def getLevels(levelDir):
    return [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(levelDir) for f in filenames]

buttons = []