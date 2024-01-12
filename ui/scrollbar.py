# external imports
import math
import pygame

# internal imports
from ui.button import Button
import input.input as input
from utils.vector2 import Vector2

class Scrollbar:
    def __init__(self, x, y, width, length, orientation, sliderWidth = None, numSteps = None, snapToSteps = False, bg = (0, 0, 0), fg = (255, 255, 255), z = 0):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.rectWidth = width if orientation == "v" else length
        self.rectHeight = length if orientation == "v" else width
        self.orientation = orientation
        self.sliderWidth = sliderWidth if sliderWidth != None else self.length / 5 #seems like a reasonable size to me
        
        self.maxStep = numSteps - 1 if numSteps is not None else None
        self.snapToSteps = snapToSteps if self.maxStep is not None else False
        
        self.bg = bg
        self.fg = fg
        self.z = z
        
        buttonWidth = self.width if self.orientation == "v" else self.sliderWidth
        buttonHeight = self.sliderWidth if self.orientation == "v" else self.width
        self.slider = Button("", self.x, self.y, buttonWidth, buttonHeight, self.fg, self.fg)
        
    def draw(self, screen, pos = Vector2(0,0)):
        x = self.x + pos.x
        y = self.y + pos.y
        pygame.draw.rect(screen, self.bg, (x, y, self.rectWidth, self.rectHeight))
        self.slider.draw(screen, pos)
    
    def moveTo(self, value):
        if self.snapToSteps:
            value = self.roundValue(value)
        
        self.setValue(value)
    
    def update(self, pos = Vector2(0,0)):
        self.slider.update(pos)
        if self.slider.held:
            wantedPos = input.mousePos.pos.y if self.orientation == "v" else input.mousePos.pos.x - self.sliderWidth / 2
            minPos = self.y if self.orientation == "v" else self.x
            maxPos = minPos + self.length-self.sliderWidth
            sliderPos = min(max(minPos, wantedPos), maxPos)
            
            if self.snapToSteps:
                sliderPos = self.roundPos(sliderPos)
            
            if self.orientation == "v":
                self.slider.y = sliderPos
            else:
                self.slider.x = sliderPos
    
    def getPos(self):
        if self.orientation == "v":
            return self.slider.y
        return self.slider.x
    
    def setPos(self, pos):
        if self.orientation == "v":
            self.slider.y = pos
        else:
            self.slider.x = pos
            
    def getValue(self):
        return self.posToValue(self.getPos())
    
    def setValue(self, value):
        self.setPos(self.valueToPos(value))
    
    def posToValue(self, pos):
        minPos = self.y if self.orientation == "v" else self.x
        maxPos = minPos + self.length-self.sliderWidth
        return (pos - minPos) / (maxPos - minPos)
    
    def valueToPos(self, value):
        minPos = self.y if self.orientation == "v" else self.x
        maxPos = minPos + self.length-self.sliderWidth
        return value * (maxPos - minPos) + minPos
    
    def posToStep(self, pos):
        return math.floor(self.posToValue(pos) * self.maxStep)
    
    def stepToPos(self, step):
        return self.valueToPos(step / self.maxStep)
    
    def roundValue(self, value):
        return math.floor(value * self.maxStep) / self.maxStep
    
    def roundPos(self, pos):
        return self.valueToPos(self.roundValue(self.posToValue(pos)))