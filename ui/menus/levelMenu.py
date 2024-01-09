import os

from graphics import gui
from ui.button import Button
from ui.popup import Popup
from ui.inputBox import InputBox
from ui.text import Text
from utils.vector2 import Vector2

popups = []
def show():
    global levels, buttons, popupOpen, popups
    if isLE: buttons.append(Button("New Level", gui.screen.get_width()/2-100, 500, 200, 50, (255,0,0), (0,0,0), newLevel))
    levels = getLevels("levels")
    levelButtons = []
    for i, level in enumerate(levels):
        levelButtons.append(genLevelButton(level, i))
    buttons += levelButtons
    
    popupOpen = False
    nLW = 500
    popups = {
        "newLevel": Popup(Vector2((1280-nLW)/2, 0), nLW, 650, 
                        [
                            InputBox("Level Name", (nLW-300)/2, 200, 300, 50, (255, 0, 0), (0,0,0), 30),
                            InputBox("Offset", (nLW-300)/2, 300, 140, 50, (255, 0, 0), (0,0,0), 30, numOnly=True),
                            InputBox("BPM", (nLW-300)/2, 350, 140, 50, (255, 0, 0), (0,0,0), 30, numOnly=True),
                            InputBox("Num", (nLW)/2+10, 300, 140, 50, (255, 0, 0), (0,0,0), 30, numOnly=True),
                            InputBox("Denom", (nLW)/2+10, 350, 140, 50, (255, 0, 0), (0,0,0), 30, numOnly=True),
                            Button("Create", (nLW-125)/2, 475, 125, 50, (255, 0, 0), (0,0,0), createLevel),
                            Button("Close", (nLW-125)/2, 550, 125, 50, (255, 0, 0), (0,0,0), popupClose),
                         ],
                        [Text("New Level", nLW/2, 100, (255, 0, 0), 40)]),
    }

isLE = False
def start(load, isLevelEditor = False):
    global loadLevel, isLE
    loadLevel = load
    isLE = isLevelEditor

def hide():
    pass

def updateFactors(factor):
    for button in buttons:
        button.factor = factor

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
    if any([inputBox.output != "" for inputBox in popups["newLevel"].objects[:5]]):
        print("filled")
    
def popupClose():
    global popups, popupOpen
    popupOpen = False
    for popup in popups.values():
        if popup.open: popup.hide()

def getLevelName(level):
    return level.split("/")[-1].split(".")[0]

def getLevels(levelDir):
    return [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(levelDir) for f in filenames]

buttons = []