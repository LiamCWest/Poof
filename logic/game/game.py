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
from graphics.particleSystem.shapedEmitter import ShapedEmitter
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
    genericParticles = ShapedEmitter(None, None, Vector2(2,2), 250, 15, 5)
    popupOpen = False
    pW = 500
    popups = {
        "pause": Popup(Vector2((1280-pW)/2, 0), pW, 650, (0,0,0), None,
                [Button("Resume", 50, 162, 400, 100, (80, 93, 112), (255, 255, 255), resume, particles=genericParticles, particlesOnOver=True, textFontPath= "ROGFONTS-REGULAR.ttf", scaler= 1.1),
                Button("Main Menu", 50, 275, 400, 100, (80, 93, 112), (255, 255, 255), lambda: gui.setScreen("main"), textFontPath= "ROGFONTS-REGULAR.ttf", scaler = 1.1),
                Button("Settings", 50, 387, 400, 100, (80, 93, 112), (255, 255 ,255), lambda: gui.setScreen("settings"), textFontPath= "ROGFONTS-REGULAR.ttf", scaler = 1.1),
                Button("Quit", 50, 500, 400, 100, (80, 93, 112), (255, 255, 255), quit, textFontPath= "ROGFONTS-REGULAR.ttf", scaler = 1.1),],
                [Text(title, 250, 80, (255, 255, 255), 100, fontPath= "ROGFONTS-REGULAR.ttf"),]),
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
    elif input.keyActionBindings["left"].justReleased:
        level.player.stopMove(Vector2(-1, 0), input.keyActionBindings["left"].songTimeLastReleased)
    
    if input.keyActionBindings["right"].justPressed:
        level.player.move(Vector2(1, 0), input.keyActionBindings["right"].songTimeLastPressed)
    elif input.keyActionBindings["right"].justReleased:
        level.player.stopMove(Vector2(1, 0), input.keyActionBindings["right"].songTimeLastReleased)
        
    if input.keyActionBindings["up"].justPressed:
        level.player.move(Vector2(0, -1), input.keyActionBindings["up"].songTimeLastPressed)
    elif input.keyActionBindings["up"].justReleased:
        level.player.stopMove(Vector2(0, -1), input.keyActionBindings["up"].songTimeLastReleased)
        
    if input.keyActionBindings["down"].justPressed:
        level.player.move(Vector2(0, 1), input.keyActionBindings["down"].songTimeLastPressed)
    elif input.keyActionBindings["down"].justReleased:
        level.player.stopMove(Vector2(0, 1), input.keyActionBindings["down"].songTimeLastReleased)

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
    if playerState.deathTime is None or playerState.deathTime + level.deathTimeBuffer >= timeSourceTime:
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize, drawPlayer=True, playerState=playerState, freezeTilesOnDeath=True)
    else:
        level.restart()
    
    accText.text = f"Acc: {int(playerState.acc * 1000)}ms   Offset: {int(abs(playerState.offset) * 1000)}ms"
    accText.draw()
    
    for popup in popups.values():
        popup.draw()
        
accText = Text("", 600, 100)