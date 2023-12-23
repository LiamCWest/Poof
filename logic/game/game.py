from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
from logic.level.level import Level
import input.input as input

tiles = [
    Tile(Vector2(0, 0), None, 1, 2, "platform"),
    Tile(Vector2(0, 1), None, 2, 3, "rest"),
    Tile(Vector2(0, 2), None, 3, 4, "wall"),
    Tile(Vector2(0, 3), None, 4, 5, "platform"),
]
level = Level(tiles, 1, 1)

def show():
    update()
    
def hide():
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        level.player.pos += Vector2(-1, 0)
    
    if input.keyBindings["right"].justPressed:
        level.player.pos += Vector2(1, 0)
        
    if input.keyBindings["up"].justPressed:
        level.player.pos += Vector2(0, -1)
        
    if input.keyBindings["down"].justPressed:
        level.player.pos += Vector2(0, 1)
    
        move(Vector2(0, -1))

def update():
    checkInput()
    draw()
    
def draw():
    level.update(gui.screen, input.getRealTime())