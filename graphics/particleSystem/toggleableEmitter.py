# internal imports
from graphics.particleSystem.shapedEmitter import ShapedEmitter #import the ShapedEmitter class
import input.input as input #import the input system

class ToggleableShapedEmitter(ShapedEmitter): #toggleable shaped emitters can be turned on and off
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5, go = False, edges = None): #initialize the toggleable shaped emitter
        ShapedEmitter.__init__(self, shape, pos, velocity, emitRate, lifeTime, size, edges = edges) #initialize the super class
        self.go = go #go determines whether or not the emitter emits
    
    def update(self): #update the particles of the emitter, and create particles if need be
        if self.go: #if the emitter should be creating particles
            if input.getRealTime() - self.lastSpawnTime > (1/self.emitRate): #if the emitter should spawn a particle,
                self.emit() #create a particle
                self.lastSpawnTime = input.getRealTime() #set the new last spawn time
        for particle in self.particles: #for each particle
            particle.update() #update the particle
            if particle.lifeTime <= 0: #if the particle should be removed
                self.particles.remove(particle) #remove the particle