#represents a scrollbar (used in settings and level editor)

# external imports
import math # for math functions
import pygame # for drawing rectangles

# internal imports
from ui.button import Button # for the scrollbar button
import input.input as input # for mouse input
from utils.vector2 import Vector2 # for vector operations

class Scrollbar: # a class representing a scrollbar
    def __init__(self, x, y, width, length, orientation, sliderWidth = None, numSteps = None, snapToSteps = False, bg = (0, 0, 0), fg = (255, 255, 255)): #constructor
        self.x = x # x position
        self.y = y # y position
        self.width = width # width of the scrollbar
        self.length = length # length of the scrollbar
        self.rectWidth = width if orientation == "v" else length # width of the scrollbar's rectangle
        self.rectHeight = length if orientation == "v" else width # height of the scrollbar's rectangle
        self.orientation = orientation # orientation of the scrollbar
        self.sliderWidth = sliderWidth if sliderWidth != None else self.length / 5 #width of the slider, length/5 seems like a reasonable default to me
        
        self.maxStep = numSteps - 1 if numSteps is not None else None #the maximum step that the scrollbar can be at
        self.snapToSteps = snapToSteps if self.maxStep is not None else False #whether or not the scrollbar should snap to steps
        
        self.bg = bg #background color
        self.fg = fg #foreground color
        
        buttonWidth = self.width if self.orientation == "v" else self.sliderWidth #width of the button
        buttonHeight = self.sliderWidth if self.orientation == "v" else self.width #height of the button
        self.slider = Button("", self.x, self.y, buttonWidth, buttonHeight, self.fg, self.fg) #the slider button
        
    def draw(self, screen, pos = Vector2(0,0)): #draw the scrollbar to the screen
        x = self.x + pos.x #x position to draw at
        y = self.y + pos.y #y position to draw at
        pygame.draw.rect(screen, self.bg, (x, y, self.rectWidth, self.rectHeight)) #draw the background of the scrollbar
        self.slider.draw(screen, pos) #draw the slider button
    
    def moveTo(self, value): #move the slider to a value
        if self.snapToSteps: #if the scrollbar should snap to steps
            value = self.roundValue(value) #round the value to the nearest step
        
        self.setValue(value) #set the value of the scrollbar
    
    def update(self, pos = Vector2(0,0)): #update the scrollbar
        self.slider.update(pos) #update the slider button
        if self.slider.held: #if the slider button is being held
            wantedPos = input.mousePos.pos.y if self.orientation == "v" else input.mousePos.pos.x - self.sliderWidth / 2 #the position that the slider wants to be at
            minPos = self.y if self.orientation == "v" else self.x #the minimum position that the slider can be at
            maxPos = minPos + self.length-self.sliderWidth #the maximum position that the slider can be at
            sliderPos = min(max(minPos, wantedPos), maxPos) #the position that the slider will be at
            
            if self.snapToSteps: #if the scrollbar should snap to steps
                sliderPos = self.roundPos(sliderPos) #round the position to the nearest step
            
            if self.orientation == "v": #if the scrollbar is vertical
                self.slider.y = sliderPos #set the slider's y position
            else: #if the scrollbar is horizontal
                self.slider.x = sliderPos #set the slider's x position
    
    def getPos(self): #get the position of the slider 
        if self.orientation == "v": #if the scrollbar is vertical
            return self.slider.y #return the slider's y position
        return self.slider.x #else return the slider's x position
    
    def setPos(self, pos): #set the position of the slider
        if self.orientation == "v": #if the scrollbar is vertical
            self.slider.y = pos #set the slider's y position
        else: #if the scrollbar is horizontal
            self.slider.x = pos #set the slider's x position
            
    def getValue(self): #get the value of the scrollbar (in range 0-1)
        return self.posToValue(self.getPos()) #return the value of the scrollbar
    
    def setValue(self, value): #set the value of the scrollbar (in range 0-1)
        self.setPos(self.valueToPos(value)) #set the position of the slider based on the value
    
    def posToValue(self, pos): #convert a position to a value (in range 0-1)
        minPos = self.y if self.orientation == "v" else self.x #the minimum position that the slider can be at
        maxPos = minPos + self.length-self.sliderWidth #the maximum position that the slider can be at
        return (pos - minPos) / (maxPos - minPos) #lerp to return the value of the scrollbar
    
    def valueToPos(self, value): #convert a value (in range 0-1) to a position
        minPos = self.y if self.orientation == "v" else self.x #the minimum position that the slider can be at
        maxPos = minPos + self.length-self.sliderWidth #the maximum position that the slider can be at
        return value * (maxPos - minPos) + minPos #lerp to return the position of the slider
    
    def posToStep(self, pos): #convert a position to a step (in range 0-maxStep)
        return math.floor(self.posToValue(pos) * self.maxStep) #return the step of the scrollbar (always an int)
    
    def stepToPos(self, step): #convert a step (in range 0-maxStep) to a position
        return self.valueToPos(step / self.maxStep) #return the position of the scrollbar
    
    def roundValue(self, value): #round a value to the nearest step
        return math.floor(value * self.maxStep) / self.maxStep #return the rounded value
    
    def roundPos(self, pos): #round a position to the nearest step by round tripping it to a value
        return self.valueToPos(self.roundValue(self.posToValue(pos))) #return the rounded position