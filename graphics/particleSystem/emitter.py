# external imports
import random #imports the random module

# internal imports
from graphics.particleSystem.particle import Particle #import the particle class
from utils.vector2 import Vector2 #import the vector2 class
import input.input as input #import the input system

class Emitter: #create the emitter class, which spawns particles
    def __init__(self, pos, velocity, emitRate, lifeTime, size=5, limit = 200): #initialize the emitter
        self.pos = pos #initialize the position
        self.velocity = velocity #initialize the velocity
        self.emitRate = emitRate #initialize the emit rate
        self.lifeTime = lifeTime #initialize the life time
        self.size = size #initialize the size of the particle
        self.limit = limit #initialize the particle object limit
        self.particles = [] #initialize the particle list, which contains the emitter's particles
        self.lastSpawnTime = 0 #initialize the last spawn time of any particle

    def emit(self): #emit a particle
        if len(self.particles) < self.limit: #check if we have enough particles
            self.particles.append(self.makeParticle()) #create a new particle

    def makeParticle(self): #create a particle
        return Particle(self.pos, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * self.velocity, self.lifeTime, self.size) #return a new particle

    def update(self): #update the emitter (create particles if need be)
        t = input.getRealTime() - self.lastSpawnTime #get the time since the last spawn
        if t <= (1/self.emitRate) * 5: #check if it's time to spawn a particle
            while t > (1/self.emitRate): #while there are more particles to spawn
                self.emit() #emit a particle
                t -= 1/self.emitRate #increment t
        self.lastSpawnTime = input.getRealTime() #set the new last spawn time
        for particle in self.particles: #for each particle in the list
            particle.update() #update the particle
            if particle.lifeTime <= 0: #if the particle should be removed
                self.particles.remove(particle) #remove the particle
            
    def draw(self, win, pos = Vector2(0,0)): #draw the particles
        for particle in self.particles: #for each particle in the list
            particle.draw(win, pos) #draw the particle

    def reset(self): #this empties the particle list
        self.particles = [] #empty the particle list