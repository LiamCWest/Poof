import pygame.mixer as mixer
import logic.song.timingPoints as timingPoints

currentTimingPoints = None

def load(songPath, timingPoints):
    global currentTimingPoints
    mixer.music.load(filename=songPath)
    currentTimingPoints = timingPoints

def unload():
    mixer.music.unload()
    
def play():
    mixer.music.play()
    
def pause():
    mixer.music.pause()
    
def seek(time):
    global lastPos
    lastPos = None
    mixer.music.rewind()
    mixer.music.set_pos(time)

lastPos = None #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos():
    global lastPos
    currentPos = mixer.music.get_pos() / 1000
    
    if lastPos is None:
        lastPos = currentPos
        return currentPos
    
    if lastPos > currentPos:
        return lastPos
    
    lastPos = currentPos
    return currentPos

def getIsPlaying():
    return mixer.music.get_busy()

def getPreviousPoint():
    global currentTimingPoints
    return timingPoints.getPreviousPoint(currentTimingPoints, getPos())

def getNextPoint():
    global currentTimingPoints
    return timingPoints.getNextPoint(currentTimingPoints, getPos())

def getPreviousBeat(divisor):
    global currentTimingPoints
    return timingPoints.getPreviousBeat(currentTimingPoints, getPos(), divisor)

def getNextBeat(divisor):
    global currentTimingPoints
    return timingPoints.getNextBeat(currentTimingPoints, getPos(), divisor)

def test():
    timingPoint1 = timingPoints.timingPoint(2.108, 170, timingPoints.timeSignature(4, 4))
    load(r"D:\Files\Godot Projects\KEYBEATS GD4\TESTFOLDER\MAPS\Abyss Of Destiny 2\Song.MP3", [timingPoint1])
    play()