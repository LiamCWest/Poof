from pynput import keyboard, mouse
import pygame
import logic.song.songPlayer as songPlayer

def getSongTime():
    return songPlayer.getPos() if songPlayer.getIsPlaying() else None
    
def getRealTime():
    ticks = pygame.time.get_ticks()
    return ticks / 1000 if ticks != 0 else None

class Event: #generic event
    def __init__(self):
        self.songTimeLastInvoked = None
        self.realTimeLastInvoked = None
        
        self.__justInvoked = False
        
    def getJustInvoked(self):
        toReturn = self.__justInvoked
        self.__justInvoked = False
        return toReturn
    
    def setJustInvoked(self, val):
        self.__justInvoked = val
    
    justInvoked = property(fget=getJustInvoked, fset=setJustInvoked)
    
    def invoke(self):
        self.justInvoked = True
        self.songTimeLastInvoked = getSongTime()
        self.realTimeLastInvoked = getRealTime()
        
    
class ButtonEvent: #keyboard keys and mouse buttons
    def __init__(self, button):
        self.button = button
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
        self.x = None
        self.y = None
        
    songTimeLastMoved = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val))
    realTimeLastMoved = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val))
    
    justMoved = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val))
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.invoke()
        
class MouseScrollEvent(Event):
    def __init__(self):
        super().__init__()
        self.dx = None
        self.dy = None
        
    songTimeLastScrolled = property(lambda self: self.songTimeLastInvoked, lambda self, val: setattr(self, "songTimeLastInvoked", val))
    realTimeLastScrolled = property(lambda self: self.realTimeLastInvoked, lambda self, val: setattr(self, "realTimeLastInvoked", val))
    
    justScrolled = property(lambda self: self.justInvoked, lambda self, val: self.setJustInvoked(val))
    
    def scroll(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.invoke()

keyBindings = {
    "left": ButtonEvent("a"),
    "up": ButtonEvent("w"),
    "right": ButtonEvent("d"),
    "down": ButtonEvent("s"),
    "dash": ButtonEvent(keyboard.Key.shift),
}

mouseBindings = {
    "lmb": ButtonEvent(mouse.Button.left),
    "mmb": ButtonEvent(mouse.Button.middle),
    "rmb": ButtonEvent(mouse.Button.right)
}

mousePos = MouseMoveEvent()
mouseScroll = MouseScrollEvent()

def onKeyPress(key):
    global keyBindings
    
    try: 
        keyValue = key.char
    except AttributeError:
        keyValue = key
    
    for event in keyBindings.values():
        if keyValue == event.button and not event.pressed:
            event.press()

def onKeyRelease(key):
    global keyBindings
    
    try: 
        keyValue = key.char
    except AttributeError:
        keyValue = key
    
    for event in keyBindings.values():
        if keyValue == event.button and event.pressed:
            event.release()
            
def onMouseClick(x, y, button, pressed):
    global mouseBindings
    
    for event in mouseBindings.values():
        if button != event.button:
            continue
        
        if pressed == event.pressed:
            continue
        
        if pressed:
            event.press()
        else:
            event.release()
            
def handleEvent(event):
    global mouseBindings
    if event.type == pygame.MOUSEMOTION:
        mousePos.move(event.pos[0], event.pos[1])
    
def onMouseScroll(x, y, dx, dy):
    global mouseScroll
    
    mouseScroll.scroll(dx, dy)

def init():
    kbListener = keyboard.Listener(on_press=onKeyPress, on_release=onKeyRelease)
    kbListener.start()
    
    mouseListener = mouse.Listener(on_click=onMouseClick, on_scroll=onMouseScroll)
    mouseListener.start()