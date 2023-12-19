import pygame.mixer as mixer

currentTimingPoints = None

def load(songPath, timingPoints):
    mixer.music.load(filename=songPath)

def unload():
    mixer.music.unload()
    
def play():
    mixer.music.play()
    
def pause():
    mixer.music.pause()
    
def seek(time):
    mixer.music.rewind()
    mixer.music.set_pos(time)
    
def get_pos():
    return mixer.music.get_pos()

