# external imports
import pygame #for getting ticks
from pynput import keyboard, mouse #for getting keyboard and mouse input
from itertools import chain #for iterating through multiple iterators at the same time

# internal imports
import logic.song.songPlayer as songPlayer #for getting song time
from utils.vector2 import Vector2 #for positions

def getSongTime(): #returns the current song time in seconds
    return songPlayer.getPos() if songPlayer.getIsPlaying() else None #return the current song time if the song is playing, else return None
    
def getRealTime(): #returns the current real time in seconds
    ticks = pygame.time.get_ticks() #get the current time in milliseconds
    return ticks / 1000 if ticks != 0 else None #return the current time in seconds if it's not 0, else return None

frameTime = None #the current frame time in seconds
oldFrameTime = None #the previous frame time in seconds
def updateFrameTimes(): #updates the frame times
    global frameTime, oldFrameTime #globals
    oldFrameTime = frameTime #set the old frame time to the current frame time
    frameTime = getRealTime() #set the current frame time to the current real time
    
def getFrameTime(): #gets the current frame time in seconds
    global frameTime #globals
    return frameTime #return the current frame time

def getOldFrameTime(): #gets the previous frame time in seconds
    global oldFrameTime #globals
    return oldFrameTime #return the previous frame time

class Event: #generic event
    def __init__(self): #constructor
        self.songTimeLastInvoked = None #the last time the event was invoked in song time
        self.realTimeLastInvoked = None #the last time the event was invoked in real time
        
        self.__justInvoked = False #whether or not the event was just invoked
        
    def getJustInvoked(self): #whether or not the event was just invoked
        toReturn = self.__justInvoked #the value to return
        self.__justInvoked = False #reset just invoked to false cause you just checked
        if self.realTimeLastInvoked is None or getOldFrameTime() is None or self.realTimeLastInvoked < getOldFrameTime(): #if it wasnt just invoked for other reasons
            return False #return false
        return toReturn #return if it was just invoked
    
    def setJustInvoked(self, val):
        self.__justInvoked = val
    
    justInvoked = property(fget=getJustInvoked, fset=setJustInvoked)
    
    def invoke(self):
        self.justInvoked = True
        self.songTimeLastInvoked = getSongTime()
        self.realTimeLastInvoked = getRealTime()
        
class ButtonEvent: #keyboard keys and mouse buttons
    def __init__(self, bindings, modifiers = None, unModifiers = None, strict = False):
        global modifierBindings
        self.bindings = bindings if isinstance(bindings, tuple) else (bindings,)
        self.modifiers = modifiers if isinstance(modifiers, tuple) else (modifiers,)
        if strict:
            unModifiers = []
            for i in modifierBindings:
                if modifiers is None or not i in modifiers:
                    unModifiers.append(i)
            self.unModifiers = tuple(unModifiers)
        else:
            self.unModifiers = unModifiers if isinstance(unModifiers, tuple) else (unModifiers,)
        self.__pressEvent = Event()
        self.__releaseEvent = Event()
        self.pressed = False
    
    songTimeLastPressed = property(lambda self: self.__pressEvent.songTimeLastInvoked, lambda self, val: setattr(self.__pressEvent, 'songTimeLastInvoked', val))
    realTimeLastPressed = property(lambda self: self.__pressEvent.realTimeLastInvoked, lambda self, val: setattr(self.__pressEvent, 'realTimeLastInvoked', val))
    songTimeLastReleased = property(lambda self: self.__releaseEvent.songTimeLastInvoked, lambda self, val: setattr(self.__releaseEvent, 'songTimeLastInvoked', val))
    realTimeLastReleased = property(lambda self: self.__releaseEvent.realTimeLastInvoked, lambda self, val: setattr(self.__releaseEvent, 'realTimeLastInvoked', val))
    
    justPressed = property(lambda self: self.__pressEvent.justInvoked, lambda self, val: self.__pressEvent.setJustInvoked(val))
    justReleased = property(lambda self: self.__releaseEvent.justInvoked, lambda self, val: self.__releaseEvent.setJustInvoked(val))
    
    def press(self):
        self.pressed = True
        self.__pressEvent.invoke()
    
    def release(self):
        self.pressed = False
        self.__releaseEvent.invoke() 
        
class MouseMoveEvent(Event):
    def __init__(self):
        super().__init__()
        self.pos = None
        
    songTimeLastMoved = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val))
    realTimeLastMoved = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val))
    
    justMoved = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val))
    
    def move(self, pos):
        self.pos = pos
        self.invoke()
        
class MouseScrollEvent(Event):
    def __init__(self):
        super().__init__()
        self.diff = None
        
    songTimeLastScrolled = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val))
    realTimeLastScrolled = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val))
    
    justScrolled = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val))
    
    def scroll(self, diff):
        self.diff = diff
        self.invoke()
        
modifierBindings = {
    "shift": ButtonEvent("Key.shift"),
    "ctrl": ButtonEvent("Key.ctrl"),
    "alt": ButtonEvent("Key.alt"),
}

characterBindings = {
    "a": ButtonEvent("'a'", strict=True),
    "b": ButtonEvent("'b'", strict=True),
    "c": ButtonEvent("'c'", strict=True),
    "d": ButtonEvent("'d'", strict=True),
    "e": ButtonEvent("'e'", strict=True),
    "f": ButtonEvent("'f'", strict=True),
    "g": ButtonEvent("'g'", strict=True),
    "h": ButtonEvent("'h'", strict=True),
    "i": ButtonEvent("'i'", strict=True),
    "j": ButtonEvent("'j'", strict=True),
    "k": ButtonEvent("'k'", strict=True),
    "l": ButtonEvent("'l'", strict=True),
    "m": ButtonEvent("'m'", strict=True),
    "n": ButtonEvent("'n'", strict=True),
    "o": ButtonEvent("'o'", strict=True),
    "p": ButtonEvent("'p'", strict=True),
    "q": ButtonEvent("'q'", strict=True),
    "r": ButtonEvent("'r'", strict=True),
    "s": ButtonEvent("'s'", strict=True),
    "t": ButtonEvent("'t'", strict=True),
    "u": ButtonEvent("'u'", strict=True),
    "v": ButtonEvent("'v'", strict=True),
    "w": ButtonEvent("'w'", strict=True),
    "x": ButtonEvent("'x'", strict=True),
    "y": ButtonEvent("'y'", strict=True),
    "z": ButtonEvent("'z'", strict=True),
    "A": ButtonEvent("'a'", "shift", strict=True),
    "B": ButtonEvent("'b'", "shift", strict=True),
    "C": ButtonEvent("'c'", "shift", strict=True),
    "D": ButtonEvent("'d'", "shift", strict=True),
    "E": ButtonEvent("'e'", "shift", strict=True),
    "F": ButtonEvent("'f'", "shift", strict=True),
    "G": ButtonEvent("'g'", "shift", strict=True),
    "H": ButtonEvent("'h'", "shift", strict=True),
    "I": ButtonEvent("'i'", "shift", strict=True),
    "J": ButtonEvent("'j'", "shift", strict=True),
    "K": ButtonEvent("'k'", "shift", strict=True),
    "L": ButtonEvent("'l'", "shift", strict=True),
    "M": ButtonEvent("'m'", "shift", strict=True),
    "N": ButtonEvent("'n'", "shift", strict=True),
    "O": ButtonEvent("'o'", "shift", strict=True),
    "P": ButtonEvent("'p'", "shift", strict=True),
    "Q": ButtonEvent("'q'", "shift", strict=True),
    "R": ButtonEvent("'r'", "shift", strict=True),
    "S": ButtonEvent("'s'", "shift", strict=True),
    "T": ButtonEvent("'t'", "shift", strict=True),
    "U": ButtonEvent("'u'", "shift", strict=True),
    "V": ButtonEvent("'v'", "shift", strict=True),
    "W": ButtonEvent("'w'", "shift", strict=True),
    "X": ButtonEvent("'x'", "shift", strict=True),
    "Y": ButtonEvent("'y'", "shift", strict=True),
    "Z": ButtonEvent("'z'", "shift", strict=True),
    
    "1": ButtonEvent("'1'", strict=True),
    "2": ButtonEvent("'2'", strict=True),
    "3": ButtonEvent("'3'", strict=True),
    "4": ButtonEvent("'4'", strict=True),
    "5": ButtonEvent("'5'", strict=True),
    "6": ButtonEvent("'6'", strict=True),
    "7": ButtonEvent("'7'", strict=True),
    "8": ButtonEvent("'8'", strict=True),
    "9": ButtonEvent("'9'", strict=True),
    "0": ButtonEvent("'0'", strict=True),
    "!": ButtonEvent("'1'", "shift", strict=True),
    "@": ButtonEvent("'2'", "shift", strict=True),
    "#": ButtonEvent("'3'", "shift", strict=True),
    "$": ButtonEvent("'4'", "shift", strict=True),
    "%": ButtonEvent("'5'", "shift", strict=True),
    "^": ButtonEvent("'6'", "shift", strict=True),
    "&": ButtonEvent("'7'", "shift", strict=True),
    "*": ButtonEvent("'8'", "shift", strict=True),
    "(": ButtonEvent("'9'", "shift", strict=True),
    ")": ButtonEvent("'0'", "shift", strict=True),
    
    "`": ButtonEvent("'`'", strict=True),
    "-": ButtonEvent("'-'", strict=True),
    "=": ButtonEvent("'='", strict=True),
    "[": ButtonEvent("'['", strict=True),
    "]": ButtonEvent("']'", strict=True),
    "\\": ButtonEvent("'\\\\'", strict=True),
    ";": ButtonEvent("';'", strict=True),
    "'": ButtonEvent("\"'\"", strict=True),
    ",": ButtonEvent("','", strict=True),
    ".": ButtonEvent("'.'", strict=True),
    "/": ButtonEvent("'/'", strict=True),
    "~": ButtonEvent("'`'", "shift", strict=True),
    "_": ButtonEvent("'-'", "shift", strict=True),
    "+": ButtonEvent("'='", "shift", strict=True),
    "{": ButtonEvent("'['", "shift", strict=True),
    "}": ButtonEvent("']'", "shift", strict=True),
    "|": ButtonEvent("'\\\\'", "shift", strict=True),
    ":": ButtonEvent("';'", strict=True),
    "\"": ButtonEvent("\"'\"", "shift", strict=True),
    "<": ButtonEvent("','", "shift", strict=True),
    ">": ButtonEvent("'.'", "shift", strict=True),
    "?": ButtonEvent("'/'", "shift", strict=True),
}

specialKeyBindings = {
    "backspace": ButtonEvent(("<8>", "<65288>"), strict=True),
    "delete": ButtonEvent(("<46>", "<65535>"), strict=True),
    "enter": ButtonEvent(("<13>", "<65293>"), strict=True),
    "escape": ButtonEvent(("<27>", "<65307>"), strict=True),
}

keyActionBindings = {
    #In game bindings
    "left": ButtonEvent("'a'"),
    "up": ButtonEvent("'w'"),
    "right": ButtonEvent("'d'"),
    "down": ButtonEvent("'s'"),
    
    #Editor bindings
    "moveTileLeft": ButtonEvent(("<37>", "<65361>", "'a'"), None, "shift"),
    "moveTileUp": ButtonEvent(("<38>", "<65362>", "'w'"), None, "shift"),
    "moveTileRight": ButtonEvent(("<39>", "<65363>", "'d'"), None, "shift"),
    "moveTileDown": ButtonEvent(("<40>", "<65364>", "'s'"), None, "shift"),
    "increaseTileLength": ButtonEvent(("<38>", "<65362>", "'w'"), "shift"),
    "decreaseTileLength": ButtonEvent(("<40>", "<65364>", "'s'"), "shift"),
    "timeBackwards": ButtonEvent(("<37>", "<65361>", "'a'"), "shift"),
    "timeForwards": ButtonEvent(("<39>", "<65363>", "'d'"), "shift"),
    "play": ButtonEvent("<32>"),
}

mouseBindings = {
    "lmb": ButtonEvent(1),
    "mmb": ButtonEvent(2),
    "rmb": ButtonEvent(3)
}

mousePos = MouseMoveEvent()
mouseScroll = MouseScrollEvent()

def toKeyStr(key):
    global kbListener
    return str(kbListener.canonical(key))

def shouldBePressed(event, keyVal):
    if any(map(lambda i: keyVal == i, event.bindings)) and not event.pressed:
        if (event.modifiers == (None,) or all(map(lambda i: modifierBindings[i].pressed, event.modifiers))):
            if(event.unModifiers == (None,) or not any(map(lambda i: modifierBindings[i].pressed, event.unModifiers))):
                return True
    return False

def shouldBeReleased(event, keyVal):
    if event.modifiers != (None,) and not all(map(lambda i: modifierBindings[i].pressed, event.modifiers)):
        return True
        
    if(event.unModifiers != (None,) and any(map(lambda i: modifierBindings[i].pressed, event.unModifiers))):
        return True
    
    if any(map(lambda i: keyVal == i, event.bindings)) and event.pressed:
        return True
    return False

def onKeyPress(key):
    global keyActionBindings, modifierBindings
    
    keyStr = toKeyStr(key)
        
    for event in modifierBindings.values():
        if any(map(lambda i: keyStr == i, event.bindings)) and not event.pressed:
            event.press()
    
    for event in chain(characterBindings.values(), specialKeyBindings.values(), keyActionBindings.values()):
        if shouldBePressed(event, keyStr):
            event.press()
            
    keyEvent = ButtonEvent(keyStr)
    keyEvent.press()

def onKeyRelease(key):
    global keyActionBindings, modifierBindings
    
    keyStr = toKeyStr(key)

    for event in modifierBindings.values():
        if any(map(lambda i: keyStr == i, event.bindings)) and event.pressed:
            event.release()
    
    for event in chain(characterBindings.values(), specialKeyBindings.values(), keyActionBindings.values()):
        if shouldBeReleased(event, keyStr):
            event.release()
            
def handleEvent(mouseEvent):
    global mouseBindings
    if mouseEvent.type == pygame.MOUSEMOTION:
        mousePos.move(Vector2(mouseEvent.pos[0], mouseEvent.pos[1]))
    elif mouseEvent.type == pygame.MOUSEWHEEL:
        mouseScroll.scroll(Vector2(mouseEvent.x, mouseEvent.y))
    elif mouseEvent.type == pygame.MOUSEBUTTONDOWN:
        for event in mouseBindings.values():
            if shouldBePressed(event, mouseEvent.button):
                event.press()
    elif mouseEvent.type == pygame.MOUSEBUTTONUP:
        for event in mouseBindings.values():
            if shouldBeReleased(event, mouseEvent.button):
                event.release()

kblistener = None
mouseListener = None
def init():
    global kbListener, mouseListener
    kbListener = keyboard.Listener(on_press=onKeyPress, on_release=onKeyRelease)
    kbListener.start()