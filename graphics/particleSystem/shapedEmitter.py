from graphics.particleSystem.particle import Particle
from graphics.particleSystem.emitter import Emitter

class ShapedEmitter(Emitter):
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5, edges = None):
        Emitter.__init__(self, pos, velocity, emitRate, lifeTime, size)
        self.shape = shape
        self.edges = edges
        
    def makeParticle(self):
        if self.shape != None and self.pos:
            if self.edges is None:
                pos = self.shape.randomPointOnEdge()
            else:
                pos = self.shape.randomPointOnParallelRectangleSides(self.edges)
            vel = self.shape.dirAt(pos) * self.velocity
            return Particle(pos + self.pos, vel, self.lifeTime, self.size)