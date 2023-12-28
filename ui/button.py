import pygame
import input.input as input

from graphics import gui
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from utils.vector2 import Vector2
from utils.polygon import Polygon

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick, onRelease = lambda: None,z = 0, particles = False, textSize = 20, scaler = 1.25):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.scale = 1
        self.scaler = scaler
        self.z = z
        self.particles = particles
        self.held = False
        self.onRelease = onRelease
        self.textSize = textSize
        
        if self.particles:
            shape = Polygon([(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
            self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(1,1), 10, 50, 5)
        
        self.textColor = textColor
        self.onClick = onClick

    def draw(self, screen):
        x = self.x - (self.width * (self.scale - 1) / 2)
        y = self.y - (self.height * (self.scale - 1) / 2)
        width = self.width * self.scale
        height = self.height * self.scale
        pygame.draw.rect(screen, self.color, (x, y, width, height))
        gui.drawText(self.text, x+width//2, y+height//2, int(self.textSize*self.scale), self.textColor)
        if self.particles:
            self.emitter.draw(screen)
        
    def isOver(self, pos):
        if pos is None:
            return False
        return self.x < pos.x < self.x + self.width and self.y < pos.y < self.y + self.height
    
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