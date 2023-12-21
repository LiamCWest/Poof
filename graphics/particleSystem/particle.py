import random
import pygame

from utils.vector2 import Vector2
from graphics.animation import Animation, AnimEvent, lerp

class Particle:
    def __init__(self, pos, lifetime, size, color):
        self.pos = pos
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.maxLifetime = lifetime
        self.moveStartedTime = input.getRealTime()
        self.moveStartedPos = self.pos
        self.targetPos = self.pos.add(self.vel.multiply(self.lifetime))
        
        moveEvent = AnimEvent(0, lifetime, self.update)
        self.moveAnim = Animation([moveEvent], self.moveStartedTime, "oneShot", lifetime)
        
    def update(self, currentTime):
        if self.lifetime <= 0:
            return
        self.pos.x = lerp(self.moveStartedPos.x, self.targetPos.x, 0, self.lifetime, currentTime)
        self.pos.y = lerp(self.moveStartedPos.y, self.targetPos.y, 0, self.lifetime, currentTime)
        
    def draw(self, screen):
        if self.lifetime <= 0:
            return
        color = colorFade(self.color, self.lifetime, self.maxLifetime)
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), self.size)
        
def colorFade(color, lifetime, maxLifetime):
    return (color[0] * (lifetime / maxLifetime), color[1] * (lifetime / maxLifetime), color[2] * (lifetime / maxLifetime))