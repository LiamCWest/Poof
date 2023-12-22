from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
import input.input as input
    
player = None

def show():
    update()
    
def hide():
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        board.move(Vector2(1, 0))
    
    if input.keyBindings["right"].justPressed:
        board.move(Vector2(-1, 0))
        
    if input.keyBindings["up"].justPressed:
        board.move(Vector2(0, 1))
        
    if input.keyBindings["down"].justPressed:
        board.move(Vector2(0, -1))
    
def update():
    draw()

def draw():
    board.draw(gui.screen)
    player.draw(gui.screen)