from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
from logic.level.level import Level
import input.input as input
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimingPoint, TimeSignature

tiles = None
level = None

def show():
    global tiles, level
    songPlayer.load(r"D:\Files\Python Projects\Poof\Poof\Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))])
    
    for i in range(10):
        print(songPlayer.getBeatByIndex(i, 1))
    
    tiles = [
        Tile(Vector2(0, 1), None, songPlayer.getBeatByIndex(0, 1), songPlayer.getBeatByIndex(1, 1), "platform"),
        Tile(Vector2(0, 2), None, songPlayer.getBeatByIndex(1, 1), songPlayer.getBeatByIndex(2, 1), "rest"),
        Tile(Vector2(1, 2), None, songPlayer.getBeatByIndex(2, 1), songPlayer.getBeatByIndex(3, 1), "wall"),
        Tile(Vector2(2, 2), None, songPlayer.getBeatByIndex(3, 1), songPlayer.getBeatByIndex(4, 1), "platform"),
    ]
    
    level = Level(tiles, 1, 1)
    
    songPlayer.play()
    update()
    
def hide():
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        level.player.move(Vector2(-1, 0), songPlayer.getPos())
    
    if input.keyBindings["right"].justPressed:
        level.player.move(Vector2(1, 0), songPlayer.getPos())
        
    if input.keyBindings["up"].justPressed:
        level.player.move(Vector2(0, -1), songPlayer.getPos())
        
    if input.keyBindings["down"].justPressed:
        level.player.move(Vector2(0, 1), songPlayer.getPos())

def update():
    checkInput()
    draw()
    
def draw():
    level.update(gui.screen, songPlayer.getPos())