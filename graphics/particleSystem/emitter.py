from graphics.particleSystem.particle import Particle
from utils.vector2 import Vector2
import random
import input.input as input

class Emitter:
    def __init__(self, pos, velocity, emitRate, lifeTime, size=5, limit = 200):
        self.pos = pos
        self.velocity = velocity
        self.emitRate = emitRate
        self.lifeTime = lifeTime
        self.size = size
        self.limit = limit
        self.particles = []
        self.lastSpawnTime = 0

    def emit(self):
        if len(self.particles) < self.limit:
            self.particles.append(self.makeParticle())

    def makeParticle(self):
        return Particle(self.pos, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * self.velocity, self.lifeTime, self.size)

    def update(self):
        t = input.getRealTime() - self.lastSpawnTime
        if t <= (1/self.emitRate) * 5:
            while t > (1/self.emitRate):
                self.emit()
                t -= 1/self.emitRate
        self.lastSpawnTime = input.getRealTime()
        for particle in self.particles:
            particle.update()
            if particle.lifeTime <= 0:
                self.particles.remove(particle)
            
    def draw(self, win, pos = Vector2(0,0)):
        for particle in self.particles:
            particle.draw(win, pos)

    def reset(self):
        self.particles = []