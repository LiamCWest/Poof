from graphics.particleSystem.particle import Particle
from graphics.particleSystem.emitter import Emitter

class ShapedEmitter(Emitter):
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5):
        Emitter.__init__(self, pos, velocity, emitRate, lifeTime, size)
        self.shape = shape
        
    def makeParticle(self):
        pos = self.shape.randomPointOnEdge()
        vel = self.shape.dirAt(pos) * self.velocity
        return Particle(pos + self.position, vel, self.lifeTime, self.size)