#the module that handles song playing

# external imports
import pygame.mixer as mixer #for playing music

songLength = None #length of song in seconds
def load(songPath): #songPath is the file path to the song
    global songLength #globals
    mixer.music.load(filename=songPath) #load the song
    song = mixer.Sound(songPath) #make a sound object so we can get the length
    songLength = song.get_length() #get the length

    seek(0) #so it's playing

def unload(): #unloads the song
    mixer.music.unload() #unloads the song
    
def getSongLength(): #returns the length of the song in seconds
    return songLength #return the length
    
def unpause(): #unpauses the song
    mixer.music.unpause() #unpauses the song
    
    global isSeekPos #globals
    isSeekPos = False #now that the song is unpaused, you're not at the seek position anymore
    
def pause(): #pauses the song
    mixer.music.pause() #pauses the song

seekPos = 0 #when play is called, it resets mixer.music.get_pos() to 0, so this is the time that was passed into seek so it can be added later
isSeekPos = False #whether or not the song is still at the seek position. this is important because if you call mixer setpos(x) then mixer getPos, it might not return exactly x
def seek(position): #seeks to the given position in seconds
    position = min(max(0, position), getSongLength()) #so position can't be before the song starts or after it ends
    
    global lastPos, seekPos, isSeekPos #globals
    lastPos = position #reset lastPos
    seekPos = position #set seekPos
    if not getIsPlaying(): #if not playing
        isSeekPos = True #then you're still at the seek position
    
    wasPlaying = getIsPlaying() #so it can keep being paused
    oldVolume = getVolume() #so it can keep the volume
    setVolume(0) #so you don't hear a random snippet of song when its seeking
    mixer.music.play(start=position) #play the song
    if not wasPlaying: #if it was paused
        mixer.music.pause() #pause it again
    setVolume(oldVolume) #so your song isnt muted

lastPos = float("-inf") #for whatever reason, the time returned by music.get_pos() can sometimes go backwards, so this makes it not do that
def getPos(): #returns the current position in seconds
    global lastPos, seekPos, isSeekPos #globals
    if isSeekPos: #if you're still at the seek position
        return seekPos #return the seek position

    currentPos = mixer.music.get_pos() / 1000 + seekPos #get the current position in seconds
    
    lastPos = max(lastPos, currentPos) #make sure time can't go backwards
    return lastPos #return the current position

def getIsPlaying(): #returns whether or not the song is playing
    return mixer.music.get_busy() #returns whether or not the song is playing

def setVolume(volume): #sets the volume
    mixer.music.set_volume(volume) #sets the volume
    
def getVolume(): #returns the volume
    return mixer.music.get_volume() #returns the volume