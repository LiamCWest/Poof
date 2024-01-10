import pygame
from graphics.animation import Animation, AnimEvent
import input.input as input
from utils.vector2 import Vector2

class Particle:
    def __init__(self, position, velocity, lifeTime, size=5, color = (255, 255, 255)):
        self.position = position
        self.velocity = velocity
        self.lifeTime = lifeTime
        self.anim_event = AnimEvent(0, self.lifeTime, self.updatePos)
        self.anim = Animation([self.anim_event], input.getRealTime(), repeatType="oneShot", length=self.lifeTime)
        self.size = size
        self.color = color
        self.factor = 1

    def updatePos(self, time):
        self.lifeTime -= time
        self.position += self.velocity.multiply(time)
        self.color = (self.color[0], self.color[1], self.color[2], 255 * (self.lifeTime/self.anim.length))
        
    def update(self):
        self.anim.updateTime(input.getRealTime())
        
    def draw(self, win, pos = Vector2(0,0)):
        newpos =  self.position.multiply(self.factor) + pos
        newpos.x -= self.size/2
        newpos.y -= self.size/2
        draw_rect_alpha(win, self.color, newpos.toTuple() + (self.size * self.factor, self.size * self.factor))
        
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)