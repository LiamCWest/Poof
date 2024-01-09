import graphics.gui as gui
from utils.vector2 import Vector2
from graphics.animation import Animation, AnimEvent, lerp, easeInOutSin
from utils.polygon import Polygon
import input.input as input

class Popup:
    def __init__(self, pos, width, height, objects = [], texts = []):
        self.pos = pos
        self.lastPos = pos
        self.width = width
        self.height = height
        self.drawPos = Vector2(pos.x,pos.y-height)
        self.objects = objects
        self.texts = texts
        self.base = Polygon.fromRect((0, 0, self.width, self.height))
        self.open = False
        self.closed = True
        
        self.moveDownTime = 1
        moveDownEvent = AnimEvent(0, self.moveDownTime, lambda time: self.moveDown(time))
        self.showAnim = Animation([moveDownEvent], 0)
        
        self.moveUpTime = 1
        moveUpEvent = AnimEvent(0, self.moveUpTime, lambda time: self.moveUp(time))
        self.closeAnim = Animation([moveUpEvent], 0)
        
    def update(self):
        if self.open:
            self.showAnim.updateTime(input.getRealTime())
            for object in self.objects:
                object.update(self.drawPos)
        elif self.closeAnim.length >= input.getRealTime()-self.closeAnim.timeSourceStartTime:
            self.closeAnim.updateTime(input.getRealTime())
        else:
            self.closed = True
            
    def draw(self):
        if not self.closed:
            self.base.draw(gui.screen, pos = self.drawPos)
            self.base.draw(gui.screen, 3, outlineColor=(255,0,0), pos = self.drawPos)
            
            for object in self.objects:
                object.draw(gui.screen, pos = self.drawPos)
                
            for text in self.texts:
                text.draw(win = gui.screen, pos = self.drawPos)
            
    def moveDown(self, time):
        self.drawPos = Vector2(self.pos.x, easeInOutSin(self.lastPos.y, self.pos.y, 0, self.moveDownTime, time))
            
    def moveUp(self, time):
        self.drawPos = Vector2(self.pos.x, easeInOutSin(self.lastPos.y, self.pos.y-self.height, 0, self.moveDownTime, time))
            
    def show(self):
        self.lastPos = self.drawPos
        self.drawPos = Vector2(self.pos.x, self.pos.y-self.height)
        self.open = True
        self.closed = False
        self.showAnim.restart(input.getRealTime())
        
    def hide(self):
        self.open = False
        self.closeAnim.restart(input.getRealTime())
        self.lastPos = self.drawPos