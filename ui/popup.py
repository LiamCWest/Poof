#a class representing a popup menu

# internal imports
import graphics.gui as gui #for drawing
from graphics.animation import Animation, AnimEvent, easeInOutSin #for animations and easing
from utils.vector2 import Vector2 #for vector operations
from utils.polygon import Polygon #for drawing polygons
import input.input as input #for mouse input

class Popup: #a class representing a popup menu
    def __init__(self, pos, width, height, color = (0,0,0), outlineColor = None, objects = [], texts = []): #constructor
        self.pos = pos #position of the popup when popped up
        self.lastPos = pos #old position of the popup
        self.width = width #width of the popup
        self.height = height #height of the popup
        self.outlineColor = outlineColor #outline color of the popup
        self.drawPos = Vector2(pos.x,0-height) #position to draw the popup at
        self.objects = objects #objects to draw in the popup
        self.texts = texts #texts to draw in the popup
        self.base = Polygon.fromRect((0, 0, self.width, self.height), color = color) #base of the popup
        self.open = False #whether or not the popup is open
        self.closed = True #whether or not the popup is closed (not exactly equal to not open, because it is only true when the popup is fully closed)
        
        self.moveDownTime = 0.75 #time it takes for the popup to move down
        moveDownEvent = AnimEvent(0, self.moveDownTime, lambda time: self.moveDown(time)) #the animation event for moving the popup down
        self.showAnim = Animation([moveDownEvent], 0) #the animation for showing the popup
        
        self.moveUpTime = 0.75 #time it takes for the popup to move up
        moveUpEvent = AnimEvent(0, self.moveUpTime, lambda time: self.moveUp(time)) #the animation event for moving the popup up
        self.closeAnim = Animation([moveUpEvent], 0) #the animation for closing the popup
        
    def update(self): #update the popup
        if self.open: #if the popup is open
            self.showAnim.updateTime(input.getRealTime()) #update the show animation
            for object in self.objects: #for each object in the popup
                object.update(self.drawPos) #update the object with the position the popup is at
        elif self.closeAnim.length >= input.getRealTime()-self.closeAnim.timeSourceStartTime: #if the popup is being closed
            self.closeAnim.updateTime(input.getRealTime()) # update the close animation
        else: #if the popup is closed
            self.closed = True #set the popup to closed
            
    def draw(self): #draw the popup
        if not self.closed: #if the popup is not closed
            self.base.draw(gui.screen, pos = self.drawPos) #draw the base of the popup
            if self.outlineColor != None: #if the popup has an outline color
                self.base.draw(gui.screen, 3, self.outlineColor, pos = self.drawPos) #draw the outline of the popup
            
            for object in self.objects: #for each object in the popup
                object.draw(gui.screen, pos = self.drawPos) #draw the object with the position the popup is at
                
            for text in self.texts: #for each text in the popup
                text.draw(win = gui.screen, pos = self.drawPos) #draw the text with the position the popup is at
            
    def moveDown(self, time): #move the popup down to a position based on a time passed in
        self.drawPos = Vector2(self.pos.x, easeInOutSin(self.lastPos.y, self.pos.y, 0, self.moveDownTime, time)) #set the position to draw the popup at
            
    def moveUp(self, time): #move the popup up to a position based on a time passed in
        self.drawPos = Vector2(self.pos.x, easeInOutSin(self.lastPos.y, 0-self.height, 0, self.moveDownTime, time)) #set the position to draw the popup at
            
    def show(self): #show the popup
        self.lastPos = self.drawPos #set the old position of the popup to the position it is currently at
        self.drawPos = Vector2(self.pos.x, 0-self.height) #set the position to draw the popup at to the top of the screen
        self.open = True #set the popup to open
        self.closed = False #set the popup to not closed
        self.showAnim.restart(input.getRealTime()) #restart the show animation
        
    def hide(self): #hide the popup
        self.open = False #set the popup to not open
        self.closeAnim.restart(input.getRealTime()) #restart the close animation
        self.lastPos = self.drawPos #set the old position of the popup to the position it is currently at