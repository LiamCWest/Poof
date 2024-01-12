# external imports
import pygame.mixer as mixer

songLength = None
def load(songPath):
    global songLength
    mixer.music.load(filename=songPath)
    song = mixer.Sound(songPath)
    songLength = song.get_length()

    seek(0) #so it's playing

def unload():
    mixer.music.unload()
    
def getSongLength():
    return songLength
    
def unpause():
    mixer.music.unpause()
    
    global isSeekPos
    isSeekPos = False
    
def pause():
    mixer.music.pause()

seekPos = 0 #when play is called, it resets mixer.music.get_pos() to 0, so this is the time that was passed into seek so it can be added later
isSeekPos = False
def seek(position):
    position = min(max(0, position), getSongLength()) #so position can't be outside the valid range
    
    global lastPos, seekPos, isSeekPos
    lastPos = position #reset lastPos
    seekPos = position #set seekPos
    if not getIsPlaying():
        isSeekPos = True
    
    wasPlaying = getIsPlaying() #so it can keep being paused
    oldVolume = getVolume()
    setVolume(0) #so you don't hear a random snippet of song when its seeking
    mixer.music.play(start=position)
    if not wasPlaying:
        mixer.music.pause()
    setVolume(oldVolume) #so your song isnt muted

lastPos = float("-inf") #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos():
    global lastPos, seekPos, isSeekPos
    if isSeekPos:
        return seekPos

    currentPos = mixer.music.get_pos() / 1000 + seekPos
    
    lastPos = max(lastPos, currentPos)
    return lastPos

def getIsPlaying():
    return mixer.music.get_busy()

def setVolume(volume):
    mixer.music.set_volume(volume)
    
def getVolume():
    return mixer.music.get_volume()