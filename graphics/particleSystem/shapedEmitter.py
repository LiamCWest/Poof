from particleSystem.particle import Particle
from particleSystem.emitter import Emitter

class ShapedEmitter(Emitter):
    def __init__(self, shape, pos, rate, maxParticles, particleLifetime, particleSize, particleColor, timeEmitting = -1):
        Emitter.__init__(self, pos, rate, maxParticles, particleLifetime, particleSize, particleColor, timeEmitting)
        self.shape = shape
        
    def makeParticle(self):
        pos = self.shape.random_point_on_edge()
        vel = self.shape.normal_at(pos).multiply(2)
        self.particles.append(Particle(pos, vel, self.particleLifetime, self.particleSize, self.particleColor))