from images import images
import pygame
from utils.vector2 import Vector2
from graphics.animation import *

class Player:
    offset = Vector2(5, 4)
    moveTime = 0.15
    def __init__(self, pos):
        self.pos = pos
        self.visiblePos = pos
        
        self.moveStartPos = pos
        self.moveStartTime = 0
        
        moveEvent = AnimEvent(0, self.moveTime, lambda time: setattr(self, "visiblePos", Vector2(easeOutPow(self.moveStartPos.x, self.pos.x, 0, self.moveTime, 3, time), easeOutPow(self.moveStartPos.y, self.pos.y, 0, self.moveTime, 3, time))))
        self.moveAnim = Animation([moveEvent], 0)
        
    def draw(self, win):
        size = Vector2(50, 50)
        img = images.images["player"]
        
        win.blit(pygame.transform.scale(img, size.toTuple()), (size * self.offset).toTuple())
        
    def move(self, diff, time):
        self.moveStartPos = self.visiblePos.copy()
        self.moveStartTime = time
        self.pos += diff
        self.moveAnim.restart(time)
        
    def updatePos(self, time):
        self.moveAnim.updateTime(time)