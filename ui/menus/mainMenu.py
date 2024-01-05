from graphics import gui
from ui.button import Button
from ui.text import Text
from ui.scrollbar import Scrollbar
from ui.menus import levelMenu
from ui.inputBox import InputBox
from logic.level import levelEditor as LE
from logic.game import game

global factor 
factor = 1

def show():
    gui.clear()
    update()

def hide():
    gui.clear()

def draw():
    objects.sort(key = lambda x : x.z)
    for object in objects:
        object.draw(gui.screen)
    for text in texts:
        text.draw()

def startGame():
    hide()
    levelMenu.setLoad(lambda level: load(level))
    gui.setScreen("levelMenu")
    def load(level):
        game.loadLevel(level)
        gui.setScreen("game")

def updateFactors(factor):
    for object in objects:
        object.factor = factor
    for text in texts:
        text.factor = factor
        
def update():
    for object in objects:
        object.update()
        
    if objects[5].returned:
        print(objects[5].output)
        objects[5].accept()
        
def settings():
    hide()
    gui.setScreen("settings")
    
def levelEditor():
    hide()
    levelMenu.setLoad(lambda level: load(level))
    gui.setScreen("levelMenu")
    def load(level):
        LE.loadLevel(level)
        gui.setScreen("levelEditor")
        
title = "Main Menu"
objects = [Button("Start", 200, 262, 200, 100, (0, 255, 0), (255, 0, 0), startGame, particles=True),
           Button("Settings", 200, 375, 200, 100, (0, 255, 0), (255, 0 ,0), settings),
           Button("Level Editor", 200, 487, 200, 100, (0, 255, 0), (255, 0, 0), levelEditor),
           Button("Quit", 200, 600, 200, 100, (0, 255, 0), (255, 0, 0), quit),
           Scrollbar(800, 75, 20, 400, "h", None, 7, True),
           InputBox("INPUT",800, 600, 200, 100, (0, 255, 0), (255, 0, 0))]
texts = [Text(title, 400, 150, (255, 0, 0), 100)]