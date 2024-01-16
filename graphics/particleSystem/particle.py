#represents a particle

# external imports
import pygame #import the pygame module

#internal imports
from graphics.animation import Animation, AnimEvent #import the animation system class
from utils.vector2 import Vector2 #import the vector2 class
import input.input as input #import the input system

class Particle: #create the class for particles
    def __init__(self, position, velocity, lifeTime, size=5, color = (255, 255, 255)): #initialize the particle
        self.position = position #set the particle's position
        self.velocity = velocity #set the particle's velocity
        self.lifeTime = lifeTime #set the particle's life time
        self.anim_event = AnimEvent(0, self.lifeTime, self.updatePos) #set the particle's animation event, which handles movement
        self.anim = Animation([self.anim_event], input.getRealTime(), repeatType="oneShot", length=self.lifeTime) #create an animation for the particle
        self.size = size #set the particle's size
        self.color = color #set the particle's color

    def updatePos(self, time): #updates the position of the particle
        self.lifeTime -= time #reduce the particle's lifetime
        self.position += self.velocity.multiply(time) #add the velocity to the particle's position
        self.color = (self.color[0], self.color[1], self.color[2], 255 * (self.lifeTime/self.anim.length)) #set the color of the particle
        
    def update(self): #updates the particle's animation
        self.anim.updateTime(input.getRealTime()) #update the animation
        
    def draw(self, win, pos = Vector2(0,0)): #draws the particle
        newpos =  self.position + pos #offset the particle's position
        newpos.x -= self.size/2 #divide the particle's position (makes it centered on x)
        newpos.y -= self.size/2 #divide the particle's position (makes it centered on y)
        draw_rect_alpha(win, self.color, newpos.toTuple() + (self.size, self.size)) #draw the rect of the particle
        
def draw_rect_alpha(surface, color, rect): #draws a rectangle
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA) #make a surface
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect()) #draws a rectangle
    surface.blit(shape_surf, rect) #blit the rectangle to the screen