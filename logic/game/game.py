from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
from logic.level.level import Level
import input.input as input
from graphics.animation import easeInPow
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimingPoint, TimeSignature
from ui.text import Text
import json
import hashlib

tiles = None
level = None
playing = False
started = False

def init():
    global started
    started = True
    level.restart()

def show():
    global level, started
    if not started: init()
    play()
    
def hide():
    gui.clear()

def loadLevel(levelFile):
    global level
    songPlayer.unload()
    level = Level.fromFile(levelFile)
    
def checkSignature(data, signature):
    return hashlib.sha256(json.dumps(data).encode()).hexdigest() == signature

def checkInput():
    if input.keyActionBindings["left"].justPressed:
        level.player.move(Vector2(-1, 0), input.keyActionBindings["left"].songTimeLastPressed)
    
    if input.keyActionBindings["right"].justPressed:
        level.player.move(Vector2(1, 0), input.keyActionBindings["right"].songTimeLastPressed)
        
    if input.keyActionBindings["up"].justPressed:
        level.player.move(Vector2(0, -1), input.keyActionBindings["up"].songTimeLastPressed)
        
    if input.keyActionBindings["down"].justPressed:
        level.player.move(Vector2(0, 1), input.keyActionBindings["down"].songTimeLastPressed)

def updateFactors(factor):
    level.factor = factor

def update():
    global playing, level, accText
    if playing:
        checkInput()
    
def pause():
    global playing
    songPlayer.pause()
    playing = False

def play():
    global playing
    songPlayer.unpause()
    playing = True

def draw():
    global accText
    timeSourceTime = songPlayer.getPos()
    
    playerState = level.player.calculateState(level, timeSourceTime)
    playerFallTime = 1
    if playerState.deathTime is None:
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize, drawPlayer=True, playerState=playerState)
    elif playerState.deathTime + level.deathTimeBuffer >= timeSourceTime:
        level.player.fallingScaler = easeInPow(1, 0, playerState.deathTime, playerState.deathTime + playerFallTime, 2, timeSourceTime)
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize, drawPlayer=True, playerState=playerState)
    else:
        level.restart()
    
    accText.text = f"{int(playerState.acc * 1000)}ms"
    accText.draw()
        
accText = Text("0ms", 100, 100)