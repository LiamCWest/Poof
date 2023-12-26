import pygame.mixer as mixer
import logic.song.timingPoints as timingPoints

currentTimingPoints = None

def load(songPath, timingPoints):
    global currentTimingPoints, song
    mixer.music.load(filename=songPath)
    song = mixer.Sound(songPath)
    currentTimingPoints = timingPoints

def unload():
    mixer.music.unload()
    
def getSongLength():
    return song.get_length()
    
def play():
    mixer.music.play()
    
def unpause():
    mixer.music.unpause()
    
def pause():
    mixer.music.pause()

def seek(position):
    global lastPos
    last_playing_state = mixer.music.get_busy()
    mixer.music.stop()
    mixer.music.play()
    mixer.music.set_pos(position)
    lastPos = position
    if last_playing_state:
        mixer.music.unpause()
    else:
        mixer.music.pause()
    print(getPos(), position)

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

def getNthPoint():
    global currentTimingPoints

def getPreviousBeat(divisor):
    global currentTimingPoints
    return timingPoints.getPreviousBeat(currentTimingPoints, getPos(), divisor)

def getNextBeat(divisor):
    global currentTimingPoints
    return timingPoints.getNextBeat(currentTimingPoints, getPos(), divisor)

def getBeatByIndex(index, divisor):
    global currentTimingPoints
    return timingPoints.getBeatByIndex(currentTimingPoints, index, divisor)

def test():
    timingPoint1 = timingPoints.TimingPoint(2.108, 170, timingPoints.TimeSignature(4, 4))
    load(r"D:\Files\Godot Projects\KEYBEATS GD4\TESTFOLDER\MAPS\Abyss Of Destiny 2\Song.MP3", [timingPoint1])
    play()