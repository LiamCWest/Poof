from graphics import gui
from ui.button import Button
from logic.game import game

def show():
    gui.setScreen("main")
    gui.clear()

def hide():
    gui.setScreen("none")
    gui.clear()

def handleEvent(event):
    for object in objects:
        object.handleEvent(event)

def draw():
    gui.drawText(title, 200, 100, 50, (255, 0, 0))
    for object in objects:
        object.draw()

def startGame():
    hide()
    game.show()
    
def update():
    for object in objects:
        object.update()
        
title = "Main Menu"
objects = [Button("Start", 100, 200, 100, 50, (0, 255, 0), (255, 0, 0), startGame),]