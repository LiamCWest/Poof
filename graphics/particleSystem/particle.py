import pygame
from graphics.animation import Animation, AnimEvent
import input.input as input

class Particle:
    def __init__(self, position, velocity, lifeTime, size=5):
        self.position = position
        self.velocity = velocity
        self.lifeTime = lifeTime
        self.anim_event = AnimEvent(0, self.lifeTime, self.updatePos)
        self.anim = Animation([self.anim_event], input.getRealTime(), repeatType="oneShot", length=self.lifeTime)
        self.size = size

    def updatePos(self, time):
        self.position += self.velocity.multiply(time)
        self.lifeTime -= time
        
    def update(self):
        self.anim.updateTime(input.getRealTime())
        
    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.position.toTuple() + (self.size, self.size))