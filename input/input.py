from pynput import keyboard
import pygame
import logic.song.songPlayer as songPlayer

class Event:
    def __init__(self, key):
        self.key = key
        
        self.pressed = False
        self.songTimeLastPressed = None
        self.songTimeLastReleased = None
        self.realTimeLastPressed = None
        self.realTimeLastReleased = None
        
        self.__justPressed = False
        self.__justReleased = False
        
    def getJustPressed(self):
        toReturn = self.__justPressed
        self.__justPressed = False
        return toReturn
    
    def setJustPressed(self, val):
        self.__justPressed = val
    
    justPressed = property(fget=getJustPressed, fset=setJustPressed)
    
    def getJustReleased(self):
        toReturn = self.__justReleased
        self.__justReleased = False
        return toReturn
    
    def setJustReleased(self, val):
        self.__justReleased = val
    
    justReleased = property(fget=getJustReleased, fset=setJustReleased)

keybinds = {
    "left": Event("'a'"),
    "up": Event("'w'"),
    "right": Event("'d'"),
    "down": Event("'s'"),
    "dash": Event("'shift'"),
}

def on_press(key):
    print(key)
    global keybinds
    
    songTime = songPlayer.getPos() if songPlayer.getIsPlaying() else None
        
    ticks = pygame.time.get_ticks()
    realTime = ticks / 1000 if ticks != 0 else None
    
    for action, event in keybinds.items():
        if str(key) == event.key and not event.pressed:
            print("pressed")
            event.songTimeLastPressed = songTime
            event.realTimeLastPressed = realTime
            event.pressed = True
            event.justPressed = True
            event.justReleased = False

def on_release(key):
    print(key)
    global keybinds
    
    songTime = songPlayer.getPos() if songPlayer.getIsPlaying() else None
        
    ticks = pygame.time.get_ticks()
    realTime = ticks / 1000 if ticks != 0 else None
    
    for action, event in keybinds.items():
        if str(key) == event.key:
            event.songTimeLastPressed = songTime
            event.realTimeLastPressed = realTime
            event.pressed = False
            event.justReleased = True
            event.justPressed = False

def init():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()