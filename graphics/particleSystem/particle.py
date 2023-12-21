import pygame

from graphics.animation import Animation, AnimEvent, lerp
import input.input as input

class Particle:
    def __init__(self, pos, vel, lifetime, size, color):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.maxLifetime = lifetime
        self.moveStartedTime = input.getRealTime()
        self.moveStartedPos = self.pos
        self.targetPos = self.pos + self.vel.multiply(self.lifetime)
        
        moveEvent = AnimEvent(0, lifetime, self.updatePos)
        self.moveAnim = Animation([moveEvent], self.moveStartedTime, "oneShot", lifetime)
        
    def update(self):
        if self.pos != self.targetPos and self.moveAnim is not None:
            self.moveAnim.updateTime(input.getRealTime())
    
    def updatePos(self, currentTime):
        self.pos.x = lerp(self.moveStartedPos.x, self.targetPos.x, 0, self.lifetime, currentTime)
        self.pos.y = lerp(self.moveStartedPos.y, self.targetPos.y, 0, self.lifetime, currentTime)
        
    def draw(self, screen):
        color = colorFade(self.color, self.lifetime, self.maxLifetime)
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), self.size)
        
def colorFade(color, lifetime, maxLifetime):
    return (color[0] * (lifetime / maxLifetime), color[1] * (lifetime / maxLifetime), color[2] * (lifetime / maxLifetime))