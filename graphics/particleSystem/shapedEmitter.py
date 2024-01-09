from graphics.particleSystem.particle import Particle
from graphics.particleSystem.emitter import Emitter

class ShapedEmitter(Emitter):
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5, H_or_V = None):
        Emitter.__init__(self, pos, velocity, emitRate, lifeTime, size)
        self.shape = shape
        self.H_or_V = H_or_V
        
    def makeParticle(self):
        if self.H_or_V is None:
            pos = self.shape.randomPointOnEdge()
        else:
            pos = self.shape.randomPointOnParallelRectangleSides(self.H_or_V)
        vel = self.shape.dirAt(pos) * self.velocity
        return Particle(pos + self.position, vel, self.lifeTime, self.size)