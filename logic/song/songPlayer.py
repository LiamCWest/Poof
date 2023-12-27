import pygame.mixer as mixer
import logic.song.timingPoints as timingPoints

currentTimingPoints = None

def load(songPath, timingPoints):
    global currentTimingPoints, song
    mixer.music.load(filename=songPath)
    song = mixer.Sound(songPath)
    currentTimingPoints = timingPoints
    
    oldVolume = getVolume()
    setVolume(0)
    play()
    unpause()
    setVolume(oldVolume)

def unload():
    mixer.music.unload()
    
def getSongLength():
    return song.get_length()
    
def play():
    global lastPos
    lastPos = float("-inf")
    mixer.music.play()
    
def stop():
    mixer.music.stop()
    
def unpause():
    mixer.music.unpause()
    
def pause():
    mixer.music.pause()
    
def seek(position):
    global lastPos
    lastPos = position
    
    wasPlaying = getIsPlaying()
    oldVolume = getVolume()
    setVolume(0)
    mixer.music.play(start=position)
    if not wasPlaying:
        mixer.music.pause()
    setVolume(oldVolume)

lastPos = float("-inf") #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos():
    global lastPos
    currentPos = mixer.music.get_pos() / 1000
    
    if lastPos > currentPos:
        return lastPos
    
    lastPos = currentPos
    return currentPos

def getIsPlaying():
    return mixer.music.get_busy()

def setVolume(volume):
    mixer.music.set_volume(volume)
    
def getVolume():
    return mixer.music.get_volume()

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

def getBeatByIndex(index, divisor):
    global currentTimingPoints
    return timingPoints.getBeatByIndex(currentTimingPoints, index, divisor) if divisor != 0 else 0

def test():
    timingPoint1 = timingPoints.TimingPoint(2.108, 170, timingPoints.TimeSignature(4, 4))
    load(r"D:\Files\Godot Projects\KEYBEATS GD4\TESTFOLDER\MAPS\Abyss Of Destiny 2\Song.MP3", [timingPoint1])
    play()