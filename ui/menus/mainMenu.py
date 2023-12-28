from graphics import gui
from ui.button import Button
from ui.text import Text
from ui.scrollbar import Scrollbar
from ui.menus import levelMenu
from logic.level import levelEditor as LE
from logic.game import game

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
    
def update():
    for object in objects:
        object.update()
        
def settings():
    hide()
    gui.setScreen("settings")
    
def levelEditor():
    hide()
    levelMenu.setLoad(lambda level: load(level))
    gui.setScreen("levelMenu")
    def load(level):
        gui.setScreen("levelEditor")
        LE.loadLevel(level)
        
title = "Main Menu"
objects = [Button("Start", 100, 175, 100, 50, (0, 255, 0), (255, 0, 0), startGame, particles=True),
           Button("Settings", 100, 250, 100, 50, (0, 255, 0), (255, 0 ,0), settings),
           Button("Level Editor", 100, 325, 100, 50, (0, 255, 0), (255, 0, 0), levelEditor),
           Button("Quit", 100, 400, 100, 50, (0, 255, 0), (255, 0, 0), quit),
           Scrollbar(400, 50, 10, 200, "h", [0,1,2,3])]
texts = [Text(title, 200, 100, (255, 0, 0), 50)]