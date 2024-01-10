from graphics.particleSystem.shapedEmitter import ShapedEmitter
import input.input as input

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