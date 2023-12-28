import os

from graphics import gui
from ui.button import Button

def show():
    global levels, levelButtons
    levels = getLevels("levels")
    levelButtons = []
    for i, level in enumerate(levels):
        levelButtons.append(genLevelButton(level, i))

def setLoad(load):
    global loadLevel
    loadLevel = load

def hide():
    pass

def update():
    for button in levelButtons:
        button.update()

def draw():
    for button in levelButtons:
        button.draw(gui.screen)

def genLevelButton(level, i):
    rowLength = 5
    x = 100 + (i % rowLength) * 100
    y = 100 + (i // rowLength) * 100
    return Button(getLevelName(level), x, y, 100, 100, (0,0,0), (255,255,255), lambda: loadLevel(level))

def getLevelName(level):
    return level.split("/")[-1].split(".")[0]

def getLevels(levelDir):
    return [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(levelDir) for f in filenames]