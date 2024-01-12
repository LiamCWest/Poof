# external imports
from copy import deepcopy

# internal imports
from ui.button import Button
from ui.text import Text
from ui.scrollbar import Scrollbar
from ui.menus import levelMenu
from ui.inputBox import InputBox
from logic.level import levelEditor as LE
from logic.game import game
from utils.vector2 import Vector2
from graphics import gui
from graphics.particleSystem.toggleableEmitter import ToggleableShapedEmitter

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
    levelMenu.start(lambda level: load(level))
    gui.setScreen("levelMenu")
    def load(level):
        game.loadLevel(level)
        gui.setScreen("game")
        
def update():
    for object in objects:
        object.update()
        
def settings():
    gui.setScreen("settings")
    
def levelEditor():
    levelMenu.start(lambda level: load(level), isLevelEditor=True)
    gui.setScreen("levelMenu")
    def load(level):
        LE.loadLevel(level)
        gui.setScreen("levelEditor")
        
title = "Main Menu"
emitter = ToggleableShapedEmitter(None, None, Vector2(4,4), 250, 25, 10, edges = "V")
objects = [Button("Start", 200, 200, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=startGame, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05),
           Button("Settings", 200, 320, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=settings, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05),
           Button("Level Editor", 200, 440, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=levelEditor, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05),
           Button("Quit", 200, 560, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=quit, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05),]
texts = [Text(title, 640, 100, (255, 255, 255), 100, font= "ROG")]