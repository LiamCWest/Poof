from graphics import gui
from objects.tile import Tile
from objects.player import Player
from utils.vector2 import Vector2
from logic.level.level import Level
import input.input as input
import logic.song.songPlayer as songPlayer
from logic.song.timingPoints import TimingPoint, TimeSignature
from ui.text import Text
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

def update():
    checkInput()
    
def draw():
    global accText
    timeSourceTime = songPlayer.getPos()
    
    playerState = level.player.calculateState(level, timeSourceTime)
    print(playerState.acc)
    
    if playerState.deathTime is None:
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize, drawPlayer=True, playerState=playerState)
    elif playerState.deathTime + level.deathTimeBuffer >= timeSourceTime:
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize)
    else:
        level.restart()
    
    accText.text = f"{int(playerState.acc * 1000)}ms"
    accText.draw()
        
accText = Text("0ms", 100, 100)