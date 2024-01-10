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
from ui.popup import Popup
from ui.button import Button
import json
import hashlib

tiles = None
level = None
playing = False
started = False
playWait = False

title = "Pause"
popups = {}
def init():
    global started, popups, popupOpen
    started = True
    
    popupOpen = False
    pW = 500
    popups = {
        "pause": Popup(Vector2((1280-pW)/2, 0), pW, 650, 
                [Button("Resume", 200, 262, 200, 100, (0, 255, 0), (255, 0, 0), resume, particles=True),
                Button("Main Menu", 200, 375, 200, 100, (0, 255, 0), (255, 0, 0), lambda: gui.setScreen("main")),
                Button("Settings", 200, 487, 200, 100, (0, 255, 0), (255, 0 ,0), lambda: gui.setScreen("settings")),
                Button("Quit", 200, 600, 200, 100, (0, 255, 0), (255, 0, 0), quit),],
                [Text(title, 400, 150, (255, 0, 0), 100)]),
    }

def show():
    global level, started, popupOpen
    if not started: 
        init()
    if not popupOpen: play()
    
def hide():
    gui.clear()

def loadLevel(levelFile):
    global level
    songPlayer.unload()
    init()
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
    global playing, popupOpen, popups, playWait
    if playing and not popupOpen:
        checkInput()
    for popup in popups.values():
        popup.update()
        
    if playWait and popups["pause"].closed:
        playWait = False
        play()
    
def pause():
    global playing, popups, popupOpen
    songPlayer.pause()
    playing = False
    
    popupOpen = True
    popups["pause"].show()

def popupClose():
    global popups, popupOpen
    popupOpen = False
    for popup in popups.values():
        if popup.open: popup.hide()

def resume():
    global playWait
    popupClose()
    playWait = True

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
    
    for popup in popups.values():
        popup.draw()
        
accText = Text("0ms", 100, 100)