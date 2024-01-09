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
        
def settings():
    gui.setScreen("settings")
    
def levelEditor():
    levelMenu.setLoad(lambda level: load(level))
    gui.setScreen("levelMenu")
    def load(level):
        LE.loadLevel(level)
        gui.setScreen("levelEditor")
        
title = "Main Menu"
objects = [Button("Start", 200, 200, 880, 100, (80, 93, 112), (255, 255, 255), startGame, particles=True, textFontPath= "ROGFONTS-REGULAR.ttf", particlesOnOver=True, scaler = 1.05),
           Button("Settings", 200, 320, 880, 100, (80, 93, 112), (255, 255, 255), settings, particles=True, textFontPath= "ROGFONTS-REGULAR.ttf", particlesOnOver=True, scaler = 1.05),
           Button("Level Editor", 200, 440, 880, 100, (80, 93, 112), (255, 255, 255), levelEditor, particles=True, textFontPath= "ROGFONTS-REGULAR.ttf", particlesOnOver=True, scaler = 1.05),
           Button("Quit", 200, 560, 880, 100, (80, 93, 112), (255, 255, 255), quit, particles=True, textFontPath= "ROGFONTS-REGULAR.ttf", particlesOnOver=True, scaler = 1.05),]
texts = [Text(title, 640, 100, (255, 255, 255), 100, fontPath= "ROGFONTS-REGULAR.ttf")]