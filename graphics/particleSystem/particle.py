import pygame
from graphics.animation import Animation, AnimEvent
import input.input as input

class Particle:
    def __init__(self, position, velocity, lifeTime):
        self.position = position
        self.velocity = velocity
        self.lifeTime = lifeTime
        self.anim_event = AnimEvent(0, self.lifeTime, self.updatePos)
        self.anim = Animation([self.anim_event], input.getRealTime(), repeatType="oneShot", length=self.lifeTime)

    def updatePos(self, time):
        self.position += self.velocity.multiply(time)
        self.lifeTime -= time
        
    def update(self):
        self.anim.updateTime(input.getRealTime())
        
    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), self.position.toTuple(), 5)