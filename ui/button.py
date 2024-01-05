import pygame
import input.input as input

from graphics import gui
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from utils.vector2 import Vector2
from utils.polygon import Polygon
from ui.text import Text
from utils.resizingFuncs import drawRectResized

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick, onRelease = lambda: None,z = 0, particles = False, textSize = 20, scaler = 1.25):
        self.text = Text(text, x + width//2, y+height//2, textColor, textSize)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.scale = 1
        self.scaler = scaler
        self.factor = 1
        self.z = z
        self.particles = particles
        self.held = False
        self.onRelease = onRelease
        
        if self.particles:
            shape = Polygon([(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
            self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(1,1), 10, 50, 5)
        
        self.onClick = onClick

    def draw(self, screen):
        x = self.x - (self.width * (self.scale - 1) / 2)
        y = self.y - (self.height * (self.scale - 1) / 2)
        width = self.width * self.scale
        height = self.height * self.scale
        drawRectResized(screen, self.color, x, y, width, height, self.factor)
        #pygame.draw.rect(screen, self.color, (x*self.factor, y*self.factor, width*self.factor, height*self.factor))
        self.text.factor = self.factor
        self.text.draw()
        if self.particles:
            self.emitter.factor = self.factor
            self.emitter.draw(screen)
        
    def isOver(self, pos):
        if pos is None:
            return False
        return (self.x * self.factor) < pos.x < ((self.x + self.width)*self.factor) and (self.y * self.factor) < pos.y < ((self.y + self.height) * self.factor)
    
    def update(self):
        if self.particles:
            self.emitter.update()

        if self.isOver(input.mousePos.pos):
            self.scale = self.scaler
            if input.mouseBindings["lmb"].justPressed:
                self.held = True
                self.onClick()
        else:
            self.scale = 1
                
        if self.held and not input.mouseBindings["lmb"].pressed:
            self.held = False
            self.onRelease()