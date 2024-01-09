import pygame
import input.input as input

from graphics import gui
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from utils.vector2 import Vector2
from utils.polygon import Polygon
from ui.text import Text
from utils.resizingFuncs import drawRectResized
from graphics.particleSystem.toggleableEmitter import ToggleableShapedEmitter

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick, onRelease = lambda: None,z = 0, particles = False, textSize = 40, scaler = 1.25, hColor = None, textFont = "Arial", particlesOnOver = False, textFontPath = None):
        self.text = Text(text, x + width//2, y+height//2, textColor, textSize, font = textFont, fontPath = textFontPath)
        self.x = x
        self.y = y
        self.width = width
        self.particlesOnOver = particlesOnOver
        self.height = height
        self.baseColor = color
        self.color = color
        self.scale = 1
        self.scaler = scaler
        self.factor = 1
        self.z = z
        self.particles = particles
        self.held = False
        self.onRelease = onRelease
        self.hColor = hColor if hColor else color
        
        if self.particles:
            w = self.width*(self.scaler-1)
            h = self.height*(self.scaler-1)
            if self.particlesOnOver:
                shape = Polygon.fromRect((0 - w/2, 0 - h/2, self.width + w, self.height + h), (255, 255, 255))
                self.emitter = ToggleableShapedEmitter(shape, Vector2(self.x, self.y), Vector2(4,4), 250, 25, 10, H_or_V = "V")
            else:
                shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255))
                self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(2,2), 100, 25, 10)
        
        self.onClick = onClick

    def draw(self, screen, pos = Vector2(0, 0)):
        x = self.x - (self.width * (self.scale - 1) / 2) + pos.x
        y = self.y - (self.height * (self.scale - 1) / 2) + pos.y
        width = self.width * self.scale
        height = self.height * self.scale
        rect = drawRectResized(screen, self.color, x, y, width, height, self.factor)
        #pygame.draw.rect(screen, self.color, (x*self.factor, y*self.factor, width*self.factor, height*self.factor))
        self.text.factor = self.factor
        self.text.scale = self.scale
        self.text.draw(rect, pos)
        if self.particles:
            self.emitter.factor = self.factor
            self.emitter.draw(screen)
        
    def isOver(self, pos, pos2):
        if pos is None:
            return False
        return (pos2.x * self.factor) < pos.x < ((pos2.x + self.width)*self.factor) and (pos2.y * self.factor) < pos.y < ((pos2.y + self.height) * self.factor)
    
    def update(self, pos = Vector2(0, 0)):
        if self.particles:
            self.emitter.update()

        canColorChange = True if self.color in [self.baseColor, self.hColor] else False
        if self.isOver(input.mousePos.pos, Vector2(self.x, self.y) + pos):
            if self.particlesOnOver:
                self.emitter.go = True
            self.scale = self.scaler
            if canColorChange: self.color = self.hColor
            if input.mouseBindings["lmb"].justPressed:
                self.held = True
                self.onClick()
        else:
            if self.particlesOnOver:
                self.emitter.go = False
            self.scale = 1
            if canColorChange: self.color = self.baseColor
                
        if self.held and not input.mouseBindings["lmb"].pressed:
            self.held = False
            self.onRelease()