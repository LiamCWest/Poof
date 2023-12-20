import random
import pygame

from utils.vector2 import Vector2

class Particle:
    def __init__(self, pos, lifetime, size, color):
        self.pos = pos
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.maxLifetime = lifetime
        
    def update(self):
        if self.lifetime <= 0:
            return
        self.pos += self.vel
        self.lifetime -= 0.01
        
    def draw(self, screen):
        if self.lifetime <= 0:
            return
        color = colorFade(self.color, self.lifetime, self.maxLifetime)
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), self.size)
        
def colorFade(color, lifetime, maxLifetime):
    return (color[0] * (lifetime / maxLifetime), color[1] * (lifetime / maxLifetime), color[2] * (lifetime / maxLifetime))