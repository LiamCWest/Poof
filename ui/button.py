import pygame
import input.input as input

from graphics import gui
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from utils.vector2 import Vector2
from utils.polygon import Polygon

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick, onRelease = lambda: None,z = 0, particles = False):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.scale = 1
        self.scaler = 1.25
        self.z = z
        self.particles = particles
        self.held = False
        self.onRelease = onRelease
        
        if self.particles:
            shape = Polygon([(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
            self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(1,1), 10, 50, 5)
        
        self.textColor = textColor
        self.onClick = onClick

    def draw(self):
        x = self.x - (self.width * (self.scale - 1) / 2)
        y = self.y - (self.height * (self.scale - 1) / 2)
        width = self.width * self.scale
        height = self.height * self.scale
        pygame.draw.rect(gui.screen, self.color, (x, y, width, height))
        gui.drawText(self.text, x+width//2, y+height//2, int(20*self.scale), self.textColor)
        if self.particles:
            self.emitter.draw(gui.screen)
        
    def isOver(self, x, y):
        if x is None or y is None:
            return False
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height
    
    def update(self):
        if self.particles:
            self.emitter.update()

        if self.isOver(input.mousePos.x, input.mousePos.y):
            if input.mouseBindings["lmb"].justPressed:
                self.onClick()
                self.held = True
            self.scale = self.scaler
        else:
            self.scale = 1
        if self.held and input.mouseBindings["lmb"].justReleased:
            self.onRelease()
            self.held = False

        self.draw()