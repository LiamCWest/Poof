import keyboard
import pygame
import logic.song.songPlayer as songPlayer

class Event:
    def __init__(self, key, eventHandler):
        self.key = key
        self.handler = eventHandler #so the key can be unbinded later
        
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
    
    justReleased = property(fget=getJustReleased, fset = setJustReleased)

keybinds = {
    "left" : Event(None, None),
    "up" : Event(None, None),
    "right" : Event(None, None),
    "down" : Event(None, None),
    "dash" : Event(None, None)
}

def bind(action, key):
    global keybinds
    def callback(event, action):
        global keybinds
        pressed = event.event_type == keyboard.KEY_DOWN
        
        if pressed == keybinds[action].pressed:
            return
        
        songTime = songPlayer.getPos() if songPlayer.getIsPlaying() else None
        
        ticks = pygame.time.get_ticks()
        realTime = ticks / 1000 if ticks != 0 else None
            
        if pressed:
            keybinds[action].songTimeLastPressed = songTime
            keybinds[action].realTimeLastPressed = realTime
            keybinds[action].pressed = True
            keybinds[action].justPressed = True
            keybinds[action].justReleased = False
        else:
            keybinds[action].songTimeLastReleased = songTime
            keybinds[action].realTimeLastReleased = realTime
            keybinds[action].pressed = False
            keybinds[action].justReleased = True
            keybinds[action].justPressed = False
            
        
    if keybinds[action].handler is not None:
        keyboard.unhook_key(keybinds[action].handler)
    newHandler = keyboard.hook_key(key, lambda event, act=action, : callback(event, act))
    keybinds[action] = Event(key, newHandler)
    
def init():
    bind("left", "a")
    bind("right", "d")
    bind("up", "w")
    bind("down", "s")
    bind("dash", "shift")