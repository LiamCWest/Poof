from graphics import gui
from ui.button import Button
from ui.text import Text
from logic.game import game
import input.input as input

def show():
    gui.clear()
    update()

def hide():
    gui.clear()

def draw():
    for object in objects:
        object.draw()
    for text in texts:
        text.draw()
        
def updateFactors(factor):
    for object in objects:
        object.factor = factor
    for text in texts:
        text.factor = factor
    
def update():
    for object in objects:
        object.update()
        
title = "Settings Menu"
objects = []
texts = [Text(title, 400, 150, (255, 0, 0), 100)]