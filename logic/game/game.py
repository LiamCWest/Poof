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
    songPlayer.load(r"Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))]) #Temp
    
    tiles = [
        Tile(Vector2(0, 0), None, 0, songPlayer.getBeatByIndex(0, 1), "platform"),
        Tile(Vector2(0, 1), None, songPlayer.getBeatByIndex(0, 1), songPlayer.getBeatByIndex(1, 1), "platform"),
        Tile(Vector2(0, 2), None, songPlayer.getBeatByIndex(1, 1), songPlayer.getBeatByIndex(2, 1), "platform"),
        Tile(Vector2(1, 2), None, songPlayer.getBeatByIndex(2, 1), songPlayer.getBeatByIndex(3, 1), "platform"),
        Tile(Vector2(2, 2), None, songPlayer.getBeatByIndex(3, 1), songPlayer.getBeatByIndex(4, 1), "platform"),
    ]
    songPlayer.unload() #Temp
    
    level = Level(tiles, 1, 1, "Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))], Vector2(0, 0), 0)
    
    level.restart()
    
    update()
    
def hide():
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        level.player.move(Vector2(-1, 0), input.keyBindings["left"].songTimeLastPressed)
    
    if input.keyBindings["right"].justPressed:
        level.player.move(Vector2(1, 0), input.keyBindings["right"].songTimeLastPressed)
        
    if input.keyBindings["up"].justPressed:
        level.player.move(Vector2(0, -1), input.keyBindings["up"].songTimeLastPressed)
        
    if input.keyBindings["down"].justPressed:
        level.player.move(Vector2(0, 1), input.keyBindings["down"].songTimeLastPressed)
        
    if input.keyBindings["dash"].justPressed:
        level.restart(0)
        level.draw(gui.screen, 0)

def update():
    checkInput()
    
def draw():
    timeSourceTime = songPlayer.getPos()
    
    playerPos = level.player.calculatePos(level, timeSourceTime)
    if isinstance(playerPos, Vector2):
        level.draw(gui.screen, timeSourceTime, level.player.calculateVisiblePos(level, timeSourceTime) - Player.offset, level.tileSize, True)
        level.player.draw(gui.screen)
    else:
        if playerPos[1] + level.deathTimeBuffer < timeSourceTime: #A buffer so you don't die unfairly if you have input delay
            level.restart()
        else:
            level.draw(gui.screen, timeSourceTime, level.player.calculateVisiblePos(level, timeSourceTime) - Player.offset, level.tileSize, False)