# internal imports
from graphics.particleSystem.particle import Particle #import the particle object
from graphics.particleSystem.emitter import Emitter #import the emitter object

class ShapedEmitter(Emitter): #shaped emitters outline a polygon
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5, edges = None): #initialize the shaped emitter
        Emitter.__init__(self, pos, velocity, emitRate, lifeTime, size) #initialize the super class
        self.shape = shape #initialize the polygon
        self.edges = edges #initialize the edges to emit from
        
    def makeParticle(self): #creates a particle on the edge of the polygon
        if self.shape != None and self.pos: #provided the shape and pos exist
            if self.edges is None: #if the shape doesn't have specified edges to emit from
                pos = self.shape.randomPointOnEdge() #get a random point on the edge of the shape
            else: #if the shape does have specified edges to emit from
                pos = self.shape.randomPointOnParallelRectangleSides(self.edges) #get a random point on one of the specified edges of the shape
            dir = self.shape.dirAt(pos) #get the direction to that point
            vel = dir * self.velocity #set the velocity
            return Particle(pos + self.pos, vel, self.lifeTime, self.size) #return the new particle