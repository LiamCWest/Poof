from graphics.particleSystem.particle import Particle
from utils.vector2 import Vector2
import random

class Emitter:
    def __init__(self, position, velocity, emitRate, lifeTime, size=5):
        self.position = position
        self.velocity = velocity
        self.emitRate = emitRate
        self.lifeTime = lifeTime
        self.size = size
        self.particles = []

    def emit(self):
        if len(self.particles) < self.emitRate:
            self.particles.append(self.makeParticle())

    def makeParticle(self):
        return Particle(self.position, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * self.velocity, self.lifeTime, self.size)

    def update(self):
        self.emit()
        for particle in self.particles:
            particle.update()
            if particle.lifeTime <= 0:
                self.particles.remove(particle)
            
    def draw(self, win):
        for particle in self.particles:
            particle.draw(win)
