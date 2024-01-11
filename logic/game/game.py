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
levelF = None

popups = {}
def init():
    global started, popups, popupOpen, win, won
    win = False
    won = False
    started = True
    genericParticles = ShapedEmitter(None, None, Vector2(2,2), 500, 15, 5)
    popupOpen = False
    pW = 500
    popups = {
        "pause": Popup(Vector2((1280-pW)/2, 0), pW, 650, (0,0,0), None,
                [Button("Resume", 50, 162, 400, 100, (80, 93, 112), (255, 255, 255), resume, particles=genericParticles, particlesOnOver=True, textFont= "ROG", scaler= 1.1),
                Button("Main Menu", 50, 275, 400, 100, (80, 93, 112), (255, 255, 255), lambda: gui.setScreen("main"), textFont= "ROG", scaler = 1.1),
                Button("Settings", 50, 387, 400, 100, (80, 93, 112), (255, 255 ,255), lambda: gui.setScreen("settings"), textFont= "ROG", scaler = 1.1),
                Button("Quit", 50, 500, 400, 100, (80, 93, 112), (255, 255, 255), quit, textFont= "ROG", scaler = 1.1),],
                [Text("Pause", 250, 80, (255, 255, 255), 100, font= "ROG"),]),
        "win": Popup(Vector2((1280-pW)/2, 0), pW, 650, (0,0,0), None,
                [Button("Restart", 50, 162, 400, 100, (80, 93, 112), (255, 255, 255), restart, particles=genericParticles, particlesOnOver=True, textFont= "ROG", scaler= 1.1),
                Button("Main Menu", 50, 275, 400, 100, (80, 93, 112), (255, 255, 255), lambda: gui.setScreen("main"), textFont= "ROG", scaler = 1.1),
                Button("Settings", 50, 387, 400, 100, (80, 93, 112), (255, 255 ,255), lambda: gui.setScreen("settings"), textFont= "ROG", scaler = 1.1),
                Button("Quit", 50, 500, 400, 100, (80, 93, 112), (255, 255, 255), quit, textFont= "ROG", scaler = 1.1),],
                [Text("You Win!", 250, 80, (255, 255, 255), 80, font= "ROG"),]),
    }

def show():
    global level, started, popupOpen
    if not started: 
        init()
    if not popupOpen: play()

def restart():
    global levelF
    popupClose()
    loadLevel(levelF)
    play()

def hide():
    gui.clear()

def loadLevel(levelFile):
    global level, endTile, levelF
    levelF = levelFile
    songPlayer.unload()
    init()
    level = Level.fromFile(levelFile)
    endTile = level.endTile()
    
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

win = False
won = False
def checkWin():
    global level, endTile, win, popups, popupOpen, playing, won
    if level.player.calculateState(level, songPlayer.getPos()).pos == endTile.pos and not won:
        win = True
    if win and endTile.disappearTime <= songPlayer.getPos():
        win = False
        songPlayer.pause()
        playing = False
        popupOpen = True
        popups["win"].show()
        won = True

def update():
    global playing, popupOpen, popups, playWait
    if playing and not popupOpen:
        checkInput()
    for popup in popups.values():
        popup.update()
    checkWin()
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
    for name, popup in popups.items():
        if popup.open and name != "win": popup.hide()

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