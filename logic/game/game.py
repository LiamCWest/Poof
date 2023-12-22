from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
import input.input as input
    
player = Player(Vector2(0, 0))
tiles = [
    Tile(Vector2(0, 0), None, 1, 2, "platform"),
    Tile(Vector2(0, 1), None, 1, 2, "rest"),
    Tile(Vector2(0, 2), None, 1, 2, "wall"),
    Tile(Vector2(0, 3), None, 1, 2, "platform"),
]

def show():
    update()
    
def hide():
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        player.pos += Vector2(-1, 0)
    
    if input.keyBindings["right"].justPressed:
        player.pos += Vector2(1, 0)
        
    if input.keyBindings["up"].justPressed:
        player.pos += Vector2(0, -1)
        
    if input.keyBindings["down"].justPressed:
        player.pos += Vector2(0, 1)
    print(player.pos)
    
def update():
    checkInput()
    draw()

def draw():
    for tile in tiles:
        tile.draw(gui.screen, player.pos)
    player.draw(gui.screen)