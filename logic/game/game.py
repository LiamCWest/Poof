from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
from logic.level.level import Level
import input.input as input
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimingPoint, TimeSignature
import json
import hashlib

tiles = None
level = None

def show():
    level.restart()
    
    update()
    
def hide():
    gui.clear()

def loadLevel(levelFile):
    global level
    songPlayer.unload()
    level = getLevel(levelFile)

def getLevel(levelFile):
    with open(levelFile, 'r') as file:
        saved_data = json.load(file)
        loaded_data = saved_data['data']
        saved_signature = saved_data['signature']
        if not checkSignature(loaded_data, saved_signature):
            print("Level file corrupted")
            return None
        tiles = loaded_data['tiles']
        tilesV2 = [Tile(Vector2.from_tuple(tile[0]), tile[1], tile[2], tile[3], tile[4]) for tile in tiles]
        appearLength = loaded_data['appearLength']
        disappearLength = loaded_data['disappearLength']
        songPath = loaded_data['songPath']
        timingPointsVals = loaded_data['timingPoints']
        timingPoints = [TimingPoint(timingPoint[0], timingPoint[1], TimeSignature(timingPoint[2], timingPoint[3])) for timingPoint in timingPointsVals]
        playerStartPos = Vector2.from_tuple(loaded_data['playerStartPos'])
        playerStartTime = loaded_data['playerStartTime']
        level = Level(tilesV2, appearLength, disappearLength, songPath, timingPoints, playerStartPos, playerStartTime)
        return level
    
def checkSignature(data, signature):
    return hashlib.sha256(json.dumps(data).encode()).hexdigest() == signature

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
        level.draw(gui.screen, timeSourceTime, level.player.calculateVisiblePos(level, timeSourceTime) - Player.offset, level.tileSize, True, False)
        level.player.draw(gui.screen)
    else:
        if playerPos[1] + level.deathTimeBuffer < timeSourceTime: #A buffer so you don't die unfairly if you have input delay
            level.restart()
        else:
            level.draw(gui.screen, timeSourceTime, level.player.calculateVisiblePos(level, timeSourceTime) - Player.offset, level.tileSize, False, False)