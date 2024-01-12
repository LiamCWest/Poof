# external imports
import pygame

# internal imports
import input.input as input
from utils.vector2 import Vector2
from utils.polygon import Polygon
from ui.text import Text

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick = lambda: None, onRelease = lambda: None,z = 0, particles = False, textSize = 40, scaler = 1.25, hColor = None, particlesOnOver = False, textFont = "ROG"):
        self.text = Text(text, x + width//2, y+height//2, textColor, textSize, font = textFont)
        self.x = x
        self.y = y
        self.width = width
        self.particlesOnOver = particlesOnOver
        self.height = height
        self.baseColor = color
        self.color = color
        self.scale = 1
        self.scaler = scaler
        self.emitter = None
        self.z = z
        self.particles = particles
        self.held = False
        self.onRelease = onRelease
        self.hColor = hColor if hColor else color
        
        if self.particles:
            self.emitter = self.particles
            
            w = self.width*(self.scaler-1)
            h = self.height*(self.scaler-1)
            
            if self.particlesOnOver:
                self.emitter.shape = Polygon.fromRect((0 - w/2, 0 - h/2, self.width + w, self.height + h), (255, 255, 255))
                #self.emitter = ToggleableShapedEmitter(shape, Vector2(self.x, self.y), Vector2(4,4), 250, 25, 10, H_or_V = "V")
            else:
                self.emitter.shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255))
                #self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(2,2), 100, 25, 10)
            
            self.emitter.pos = Vector2(self.x, self.y)
        
        self.onClick = onClick

    def draw(self, screen, pos = Vector2(0, 0)):
        x = self.x - (self.width * (self.scale - 1) / 2) + pos.x
        y = self.y - (self.height * (self.scale - 1) / 2) + pos.y
        width = self.width * self.scale
        height = self.height * self.scale
        if self.particles:
            self.emitter.draw(screen, pos)
        rect = pygame.draw.rect(screen, self.color, (x, y, width, height))
        self.text.scale = self.scale
        self.text.draw(rect, pos)
        
    def isOver(self, pos, pos2):
        if pos is None:
            return False
        return pos2.x < pos.x < (pos2.x + self.width) and pos2.y < pos.y < pos2.y + self.height
    
    def update(self, pos = Vector2(0, 0)):
        if self.particles:
            self.emitter.update()

        canColorChange = True if self.color in [self.baseColor, self.hColor] else False
        if self.isOver(input.mousePos.pos, Vector2(self.x, self.y) + pos):
            if self.particlesOnOver:
                self.emitter.go = True
            if self.emitter:
                w = self.width*(self.scaler-1)
                h = self.height*(self.scaler-1)
                self.emitter.shape = Polygon.fromRect((0 - w/2, 0 - h/2, self.width + w, self.height + h), (255, 255, 255))
            self.scale = self.scaler
            if canColorChange: self.color = self.hColor
            if input.mouseBindings["lmb"].justPressed:
                self.held = True
                self.onClick()
        else:
            if self.particlesOnOver:
                self.emitter.go = False
            self.scale = 1
            if self.emitter:
                self.emitter.shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255))
            if canColorChange: self.color = self.baseColor
                
        if self.held and not input.mouseBindings["lmb"].pressed:
            self.held = False
            self.onRelease()