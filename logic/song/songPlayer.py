import pygame.mixer as mixer
import timingPoints

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
    mixer.music.rewind()
    mixer.music.set_pos(time)
    
def getPos():
    return mixer.music.get_pos()

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