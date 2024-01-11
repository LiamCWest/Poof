import pygame
import input.input as input

from graphics import gui
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from utils.vector2 import Vector2
from utils.polygon import Polygon
from ui.text import Text

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick, onRelease = lambda: None,z = 0, particles = False, textSize = 40, scaler = 1.25):
        self.text = Text(text, x + width//2, y+height//2, textColor, textSize)
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
        
        if self.particles:
            shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255))
            self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(1,1), 10, 50, 5)
        
        self.onClick = onClick

    def draw(self, screen, pos = Vector2(0, 0)):
        x = self.x - (self.width * (self.scale - 1) / 2) + pos.x
        y = self.y - (self.height * (self.scale - 1) / 2) + pos.y
        width = self.width * self.scale
        height = self.height * self.scale
        rect = pygame.draw.rect(screen, self.color, (x, y, width, height))
        self.text.scale = self.scale
        self.text.draw(rect, pos)
        if self.particles:
            self.emitter.draw(screen)
        
    def isOver(self, pos, pos2):
        if pos is None:
            return False
        return pos2.x < pos.x < (pos2.x + self.width) and pos2.y < pos.y < pos2.y + self.height
    
    def update(self, pos = Vector2(0, 0)):
        if self.particles:
            self.emitter.update()

        if self.isOver(input.mousePos.pos, Vector2(self.x, self.y) + pos):
            self.scale = self.scaler
            if input.mouseBindings["lmb"].justPressed:
                self.held = True
                self.onClick()
        else:
            self.scale = 1
                
        if self.held and not input.mouseBindings["lmb"].pressed:
            self.held = False
            self.onRelease()