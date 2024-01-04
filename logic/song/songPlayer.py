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

addPos = 0 #when play is called, it resets get_pos() to 0, so this is the time from when play was called to when the song actually starts playing
def seek(position):
    global lastPos, addPos
    lastPos = position
    
    wasPlaying = getIsPlaying()
    oldVolume = getVolume()
    setVolume(0)
    mixer.music.play(start=position)
    addPos = position
    if not wasPlaying:
        mixer.music.pause()
    setVolume(oldVolume)

lastPos = float("-inf") #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos():
    global lastPos
    currentPos = mixer.music.get_pos() / 1000 + addPos
    
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

def getPreviousBeat(divisor, time = None):
    global currentTimingPoints
    if time is None:
        time = getPos()
    return timingPoints.getPreviousBeat(currentTimingPoints, time, divisor)

def getNextBeat(divisor, time = None):
    global currentTimingPoints
    if time is None:
        time = getPos()
    return timingPoints.getNextBeat(currentTimingPoints, time, divisor)

def getNearestBeat(divisor, time = None):
    global currentTimingPoints
    if time is None:
        time = getPos()
    return timingPoints.getNearestBeat(currentTimingPoints, time, divisor)

def test():
    timingPoint1 = timingPoints.TimingPoint(2.108, 170, timingPoints.TimeSignature(4, 4))
    load(r"D:\Files\Godot Projects\KEYBEATS GD4\TESTFOLDER\MAPS\Abyss Of Destiny 2\Song.MP3", [timingPoint1])
    play()