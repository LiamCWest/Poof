# internal imports
from graphics.particleSystem.shapedEmitter import ShapedEmitter
from graphics.particleSystem.emitter import Emitter
import input.input as input

class ToggleableEmitter(Emitter):
    def __init__(self, pos, velocity, emitRate, lifeTime, size=5, go = False, directionRange = (0,0)):
        Emitter.__init__(self, pos, velocity, emitRate, lifeTime, size, directionRange=directionRange)
        self.go = go
    
    def update(self):
        if self.go:
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
                
class ToggleableShapedEmitter(ShapedEmitter):
    def __init__(self, shape, pos, velocity, emitRate, lifeTime, size=5, go = False, edges = None):
        ShapedEmitter.__init__(self, shape, pos, velocity, emitRate, lifeTime, size, edges = edges)
        self.go = go
    
    def update(self):
        if self.go:
            if input.getRealTime() - self.lastSpawnTime > (1/self.emitRate):
                self.emit()
                self.lastSpawnTime = input.getRealTime()
        for particle in self.particles:
            particle.update()
            if particle.lifeTime <= 0:
                self.particles.remove(particle)