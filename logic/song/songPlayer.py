import pygame.mixer as mixer
import logic.song.timingPoints as timingPoints

currentTimingPoints = None
songLength = None
def load(songPath, timingPoints):
    global currentTimingPoints, songLength
    mixer.music.load(filename=songPath)
    song = mixer.Sound(songPath)
    songLength = song.get_length()
    currentTimingPoints = timingPoints

    seek(0) #so it's playing

def unload():
    mixer.music.unload()
    
def getSongLength():
    return songLength
    
def unpause():
    mixer.music.unpause()
    
def pause():
    mixer.music.pause()

seekPos = 0 #when play is called, it resets mixer.music.get_pos() to 0, so this is the time that was passed into seek so it can be added later
def seek(position):
    position = min(max(0, position), getSongLength()) #so position can't be outside the valid range
    
    global lastPos, seekPos
    lastPos = position #reset lastPos
    seekPos = position #set seekPos
    
    wasPlaying = getIsPlaying() #so it can keep being paused
    oldVolume = getVolume()
    setVolume(0) #so you don't hear a random snippet of song when its seeking
    mixer.music.play(start=position)
    if not wasPlaying:
        mixer.music.pause()
    setVolume(oldVolume) #so your song isnt muted

lastPos = float("-inf") #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos():
    global lastPos
    currentPos = mixer.music.get_pos() / 1000 + seekPos
    
    lastPos = max(lastPos, currentPos)
    return lastPos

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