#the module that handles input

# external imports
import pygame #for getting ticks
from pynput import keyboard #for getting keyboard input
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
        
        self.__justInvoked = False #whether or not the event was just invoked (private, hidden by property)
        
    def getJustInvoked(self): #whether or not the event was just invoked
        toReturn = self.__justInvoked #the value to return
        self.__justInvoked = False #reset just invoked to false cause you just checked
        if self.realTimeLastInvoked is None or getOldFrameTime() is None or self.realTimeLastInvoked < getOldFrameTime(): #if it wasnt just invoked for other reasons
            return False #return false
        return toReturn #return if it was just invoked
    
    def setJustInvoked(self, val): #sets if the event was just invoked
        self.__justInvoked = val #set just invoked to the value
    
    justInvoked = property(fget=getJustInvoked, fset=setJustInvoked) #a public property for justInvoked
    
    def invoke(self): #invokes the event
        self.justInvoked = True #the event is just invoked
        self.songTimeLastInvoked = getSongTime() #it was invoked at the current song time
        self.realTimeLastInvoked = getRealTime() #it was invoked at the current real time
        
class ButtonEvent: #an event for keyboard keys and mouse buttons
    def __init__(self, bindings, modifiers = None, unModifiers = None, strict = False): #constructor
        global modifierBindings #globals
        self.bindings = bindings if isinstance(bindings, tuple) else (bindings,) #the bindings that can trigger the event
        self.modifiers = modifiers if isinstance(modifiers, tuple) else (modifiers,) #the modifier keys that need to be pressed to trigger the event
        if strict: #no other modifier keys can be pressed
            unModifiers = [] #the unmodifiers (modifier keys that can't be pressed)
            for i in modifierBindings: #for each possible modifier key
                if modifiers is None or not i in modifiers: #if the modifier key isn't in the modifiers
                    unModifiers.append(i) #add it to the unmodifiers
            self.unModifiers = tuple(unModifiers) #set the unmodifiers
        else: #other modifier keys can be pressed
            self.unModifiers = unModifiers if isinstance(unModifiers, tuple) else (unModifiers,) #the unmodifiers (modifier keys that can't be pressed)
        self.__pressEvent = Event() #the event for when the button is pressed
        self.__releaseEvent = Event() #the event for when the button is released
        self.pressed = False #whether or not the button is pressed
    
    songTimeLastPressed = property(lambda self: self.__pressEvent.songTimeLastInvoked, lambda self, val: setattr(self.__pressEvent, 'songTimeLastInvoked', val)) #the last time the button was pressed in song time (alias of the press event's song time last invoked)
    realTimeLastPressed = property(lambda self: self.__pressEvent.realTimeLastInvoked, lambda self, val: setattr(self.__pressEvent, 'realTimeLastInvoked', val)) #the last time the button was pressed in real time (alias of the press event's real time last invoked)
    songTimeLastReleased = property(lambda self: self.__releaseEvent.songTimeLastInvoked, lambda self, val: setattr(self.__releaseEvent, 'songTimeLastInvoked', val)) #the last time the button was released in song time (alias of the release event's song time last invoked)
    realTimeLastReleased = property(lambda self: self.__releaseEvent.realTimeLastInvoked, lambda self, val: setattr(self.__releaseEvent, 'realTimeLastInvoked', val)) #the last time the button was released in real time (alias of the release event's real time last invoked)
    
    justPressed = property(lambda self: self.__pressEvent.justInvoked, lambda self, val: self.__pressEvent.setJustInvoked(val)) #whether or not the button was just pressed (alias of the press event's just invoked)
    justReleased = property(lambda self: self.__releaseEvent.justInvoked, lambda self, val: self.__releaseEvent.setJustInvoked(val)) #whether or not the button was just released (alias of the release event's just invoked)
    
    def press(self): #presses the button
        self.pressed = True #the button is pressed
        self.__pressEvent.invoke() #invoke the press event
    
    def release(self): #releases the button
        self.pressed = False #the button is not pressed
        self.__releaseEvent.invoke() #invoke the release event
        
class MouseMoveEvent(Event): #an event for mouse movement
    def __init__(self): #constructor
        super().__init__() #init base
        self.pos = None #the position of the mouse (currently none as it hasn't ever been moved)
        
    songTimeLastMoved = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val)) #the last time the mouse was moved in song time (alias of the song time last invoked)
    realTimeLastMoved = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val)) #the last time the mouse was moved in real time (alias of the real time last invoked)
    
    justMoved = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val)) #whether or not the mouse was just moved (alias of the just invoked)
    
    def move(self, pos): #moves the mouse
        self.pos = pos #set the position of the mouse to the position passed in
        self.invoke() #invoke own event
        
class MouseScrollEvent(Event): #an event for mouse scrolling
    def __init__(self): #constructor
        super().__init__() #init base
        self.diff = None #the difference in scroll (currently none as it hasn't ever been scrolled)
        
    songTimeLastScrolled = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val)) #the last time the mouse was scrolled in song time (alias of the song time last invoked)
    realTimeLastScrolled = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val)) #the last time the mouse was scrolled in real time (alias of the real time last invoked)
    
    justScrolled = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val)) #whether or not the mouse was just scrolled (alias of the just invoked)
     
    def scroll(self, diff): #scrolls the mouse
        self.diff = diff #set the difference in scroll to the difference in scroll passed in
        self.invoke() #invoke own event
        
modifierBindings = { #all modifier keybindings
    "shift": ButtonEvent("Key.shift"), #the shift key
    "ctrl": ButtonEvent("Key.ctrl"), #the control key
    "alt": ButtonEvent("Key.alt"), #the alt key
}

characterBindings = { #all character keybindings (bindings that produce a character when pressed)
    "a": ButtonEvent("'a'", strict=True), #the character a
    "b": ButtonEvent("'b'", strict=True), #the character b
    "c": ButtonEvent("'c'", strict=True), #the character c
    "d": ButtonEvent("'d'", strict=True), #the character d
    "e": ButtonEvent("'e'", strict=True), #the character e
    "f": ButtonEvent("'f'", strict=True), #the character f
    "g": ButtonEvent("'g'", strict=True), #the character g
    "h": ButtonEvent("'h'", strict=True), #the character h
    "i": ButtonEvent("'i'", strict=True), #the character i
    "j": ButtonEvent("'j'", strict=True), #the character j
    "k": ButtonEvent("'k'", strict=True), #the character k
    "l": ButtonEvent("'l'", strict=True), #the character l
    "m": ButtonEvent("'m'", strict=True), #the character m
    "n": ButtonEvent("'n'", strict=True), #the character n
    "o": ButtonEvent("'o'", strict=True), #the character o
    "p": ButtonEvent("'p'", strict=True), #the character p
    "q": ButtonEvent("'q'", strict=True), #the character q
    "r": ButtonEvent("'r'", strict=True), #the character r
    "s": ButtonEvent("'s'", strict=True), #the character s
    "t": ButtonEvent("'t'", strict=True), #the character t
    "u": ButtonEvent("'u'", strict=True), #the character u
    "v": ButtonEvent("'v'", strict=True), #the character v
    "w": ButtonEvent("'w'", strict=True), #the character w
    "x": ButtonEvent("'x'", strict=True), #the character x
    "y": ButtonEvent("'y'", strict=True), #the character y
    "z": ButtonEvent("'z'", strict=True), #the character z
    "A": ButtonEvent("'a'", "shift", strict=True), #the character A (shift + a)
    "B": ButtonEvent("'b'", "shift", strict=True), #the character B (shift + b)
    "C": ButtonEvent("'c'", "shift", strict=True), #the character C (shift + c)
    "D": ButtonEvent("'d'", "shift", strict=True), #the character D (shift + d)
    "E": ButtonEvent("'e'", "shift", strict=True), #the character E (shift + e)
    "F": ButtonEvent("'f'", "shift", strict=True), #the character F (shift + f)
    "G": ButtonEvent("'g'", "shift", strict=True), #the character G (shift + g)
    "H": ButtonEvent("'h'", "shift", strict=True), #the character H (shift + h)
    "I": ButtonEvent("'i'", "shift", strict=True), #the character I (shift + i)
    "J": ButtonEvent("'j'", "shift", strict=True), #the character J (shift + j)
    "K": ButtonEvent("'k'", "shift", strict=True), #the character K (shift + k)
    "L": ButtonEvent("'l'", "shift", strict=True), #the character L (shift + l)
    "M": ButtonEvent("'m'", "shift", strict=True), #the character M (shift + m)
    "N": ButtonEvent("'n'", "shift", strict=True), #the character N (shift + n)
    "O": ButtonEvent("'o'", "shift", strict=True), #the character O (shift + o)
    "P": ButtonEvent("'p'", "shift", strict=True), #the character P (shift + p)
    "Q": ButtonEvent("'q'", "shift", strict=True), #the character Q (shift + q)
    "R": ButtonEvent("'r'", "shift", strict=True), #the character R (shift + r)
    "S": ButtonEvent("'s'", "shift", strict=True), #the character S (shift + s)
    "T": ButtonEvent("'t'", "shift", strict=True), #the character T (shift + t)
    "U": ButtonEvent("'u'", "shift", strict=True), #the character U (shift + u)
    "V": ButtonEvent("'v'", "shift", strict=True), #the character V (shift + v)
    "W": ButtonEvent("'w'", "shift", strict=True), #the character W (shift + w)
    "X": ButtonEvent("'x'", "shift", strict=True), #the character X (shift + x)
    "Y": ButtonEvent("'y'", "shift", strict=True), #the character Y (shift + y)
    "Z": ButtonEvent("'z'", "shift", strict=True), #the character Z (shift + z)
    
    "1": ButtonEvent("'1'", strict=True), #the character 1
    "2": ButtonEvent("'2'", strict=True), #the character 2
    "3": ButtonEvent("'3'", strict=True), #the character 3
    "4": ButtonEvent("'4'", strict=True), #the character 4
    "5": ButtonEvent("'5'", strict=True), #the character 5
    "6": ButtonEvent("'6'", strict=True), #the character 6
    "7": ButtonEvent("'7'", strict=True), #the character 7
    "8": ButtonEvent("'8'", strict=True), #the character 8
    "9": ButtonEvent("'9'", strict=True), #the character 9
    "0": ButtonEvent("'0'", strict=True), #the character 0
    "!": ButtonEvent("'1'", "shift", strict=True), #the character ! (shift + 1)
    "@": ButtonEvent("'2'", "shift", strict=True), #the character @ (shift + 2)
    "#": ButtonEvent("'3'", "shift", strict=True), #the character # (shift + 3)
    "$": ButtonEvent("'4'", "shift", strict=True), #the character $ (shift + 4)
    "%": ButtonEvent("'5'", "shift", strict=True), #the character % (shift + 5)
    "^": ButtonEvent("'6'", "shift", strict=True), #the character ^ (shift + 6)
    "&": ButtonEvent("'7'", "shift", strict=True), #the character & (shift + 7)
    "*": ButtonEvent("'8'", "shift", strict=True), #the character * (shift + 8)
    "(": ButtonEvent("'9'", "shift", strict=True), #the character ( (shift + 9)
    ")": ButtonEvent("'0'", "shift", strict=True), #the character ) (shift + 0)
    
    "`": ButtonEvent("'`'", strict=True), #the character `
    "-": ButtonEvent("'-'", strict=True), #the character -
    "=": ButtonEvent("'='", strict=True), #the character =
    "[": ButtonEvent("'['", strict=True), #the character [
    "]": ButtonEvent("']'", strict=True), #the character ]
    "\\": ButtonEvent("'\\\\'", strict=True), #the character \
    ";": ButtonEvent("';'", strict=True), #the character ;
    "'": ButtonEvent("\"'\"", strict=True), #the character '
    ",": ButtonEvent("','", strict=True), #the character ,
    ".": ButtonEvent("'.'", strict=True), #the character .
    "/": ButtonEvent("'/'", strict=True), #the character /
    "~": ButtonEvent("'`'", "shift", strict=True), #the character ~ (shift + `)
    "_": ButtonEvent("'-'", "shift", strict=True), #the character _ (shift + -)
    "+": ButtonEvent("'='", "shift", strict=True), #the character + (shift + =)
    "{": ButtonEvent("'['", "shift", strict=True), #the character { (shift + [)
    "}": ButtonEvent("']'", "shift", strict=True), #the character } (shift + ])
    "|": ButtonEvent("'\\\\'", "shift", strict=True), #the character | (shift + \)
    ":": ButtonEvent("';'", strict=True), #the character : (shift + ;)
    "\"": ButtonEvent("\"'\"", "shift", strict=True), #the character " (shift + ')
    "<": ButtonEvent("','", "shift", strict=True), #the character < (shift + ,)
    ">": ButtonEvent("'.'", "shift", strict=True), #the character > (shift + .)
    "?": ButtonEvent("'/'", "shift", strict=True), #the character ? (shift + /)
    
    " ": ButtonEvent("<32>", strict=False) #the character " " (only character not affected by shift)
}

specialKeyBindings = { #all special keybindings (bindings that don't produce a character when pressed, but aren't modifiers)
    "backspace": ButtonEvent(("<8>", "<65288>"), strict=True), #backspace (with linux and windows keycodes)
    "delete": ButtonEvent(("<46>", "<65535>"), strict=True), #delete (with linux and windows keycodes)
    "enter": ButtonEvent(("<13>", "<65293>"), strict=True), #enter (with linux and windows keycodes)
    "escape": ButtonEvent(("<27>", "<65307>"), strict=True), #escape (with linux and windows keycodes)
}

mouseBindings = { #all mouse button bindings
    "lmb": ButtonEvent(1), #left mouse button
    "mmb": ButtonEvent(2), #middle mouse button
    "rmb": ButtonEvent(3) #right mouse button
}

mousePos = MouseMoveEvent() #the mouse position
mouseScroll = MouseScrollEvent() #the mouse scroll

keyActionBindings = { #all key action bindings (bindings that produce an action in game)
    #In game bindings
    "left": ButtonEvent(("<37>", "<65361>", "'a'")), #moves player left
    "up": ButtonEvent(("<38>", "<65362>", "'w'")), #moves player up
    "right": ButtonEvent(("<39>", "<65363>", "'d'")), #moves player right
    "down": ButtonEvent(("<40>", "<65364>", "'s'")), #moves player down
    
    #Editor bindings
    "moveTileLeft": ButtonEvent(("<37>", "<65361>", "'a'"), None, "shift"), #moves the selected tile left in editor
    "moveTileUp": ButtonEvent(("<38>", "<65362>", "'w'"), None, "shift"), #moves the selected tile up in editor
    "moveTileRight": ButtonEvent(("<39>", "<65363>", "'d'"), None, "shift"), #moves the selected tile right in editor
    "moveTileDown": ButtonEvent(("<40>", "<65364>", "'s'"), None, "shift"), #moves the selected tile down in editor
    "increaseTileLength": ButtonEvent(("<38>", "<65362>", "'w'"), "shift"), #increases the length of the selected tile in editor
    "decreaseTileLength": ButtonEvent(("<40>", "<65364>", "'s'"), "shift"), #decreases the length of the selected tile in editor
    "timeBackwards": ButtonEvent(("<37>", "<65361>", "'a'"), "shift"), #moves the song time backwards in editor
    "timeForwards": ButtonEvent(("<39>", "<65363>", "'d'"), "shift"), #moves the song time forwards in editor
    "play": ButtonEvent("<32>"), #plays the song in editor
}

def toKeyStr(key): #converts a kblistener key to a string for comparison with the dictionary keys
    global kbListener #globals
    return str(kbListener.canonical(key)) #return the string representation of the canonical representation of the key

def shouldBePressed(event, keyVal): #if an event should be pressed based on the state of the keyboard
    if any(map(lambda i: keyVal == i, event.bindings)) and not event.pressed: #if the key pressed is in the bindings and the event isn't pressed
        if (event.modifiers == (None,) or all(map(lambda i: modifierBindings[i].pressed, event.modifiers))): #if all the modifiers are pressed
            if(event.unModifiers == (None,) or not any(map(lambda i: modifierBindings[i].pressed, event.unModifiers))): #if none of the unmodifiers are pressed
                return True #it should be pressed
    return False #else it shouldn't be pressed

def shouldBeReleased(event, keyVal): #if an event should be released based on the state of the keyboard
    if not event.pressed: #if the event is already released
        return False #it shouldn't be released
    
    if event.modifiers != (None,) and not all(map(lambda i: modifierBindings[i].pressed, event.modifiers)): #if any of the modifiers aren't pressed
        return True #it should be released
        
    if(event.unModifiers != (None,) and any(map(lambda i: modifierBindings[i].pressed, event.unModifiers))): #if any of the unmodifiers are pressed
        return True #it should be released
    
    if any(map(lambda i: keyVal == i, event.bindings)): #if the key released is in the bindings
        return True #it should be released
    return False #else it shouldn't be released

def onKeyPress(key): #called by pynput when a key is pressed
    global keyActionBindings, modifierBindings #globals
    
    keyStr = toKeyStr(key) #get the string representation of the key

    for event in modifierBindings.values(): #for each modifier key
        if any(map(lambda i: keyStr == i, event.bindings)) and not event.pressed: #if the key pressed is in the bindings and the event isn't pressed
            event.press() #press the event
    
    for event in chain(characterBindings.values(), specialKeyBindings.values(), keyActionBindings.values()): #for each event
        if shouldBePressed(event, keyStr): #if the event should be pressed
            event.press() #press the event

def onKeyRelease(key): #called by pynput when a key is released
    global keyActionBindings, modifierBindings #globals
    
    keyStr = toKeyStr(key) #get the string representation of the key

    for event in modifierBindings.values(): #for each modifier key
        if any(map(lambda i: keyStr == i, event.bindings)) and event.pressed: #if the key released is in the bindings and the event is pressed
            event.release() #release the event
    
    for event in chain(characterBindings.values(), specialKeyBindings.values(), keyActionBindings.values()): #for each event
        if shouldBeReleased(event, keyStr): #if the event should be released
            event.release() #release the event
            
def handleEvent(mouseEvent): #handles mouse events (called by pygame) because pynput can't handle mouse events very well
    global mouseBindings #globals
    if mouseEvent.type == pygame.MOUSEMOTION: #if the mouse was moved
        mousePos.move(Vector2(mouseEvent.pos[0], mouseEvent.pos[1])) #move the mouse
    elif mouseEvent.type == pygame.MOUSEWHEEL: #if the mouse was scrolled
        mouseScroll.scroll(Vector2(mouseEvent.x, mouseEvent.y)) #scroll the mouse
    elif mouseEvent.type == pygame.MOUSEBUTTONDOWN: #if a mouse button was pressed
        for event in mouseBindings.values(): #for each mouse button event
            if shouldBePressed(event, mouseEvent.button): #if the event should be pressed
                event.press() #press the event
    elif mouseEvent.type == pygame.MOUSEBUTTONUP: #if a mouse button was released
        for event in mouseBindings.values(): #for each mouse button event
            if shouldBeReleased(event, mouseEvent.button): #if the event should be released
                event.release() #release the event

kblistener = None #the keyboard listener
def init(): #initializes the input module
    global kbListener, mouseListener #globals
    kbListener = keyboard.Listener(on_press=onKeyPress, on_release=onKeyRelease) #create the keyboard listener
    kbListener.start() #start the keyboard listener