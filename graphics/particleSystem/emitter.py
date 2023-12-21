from graphics.particleSystem.particle import Particle

class ParticleEmitter:
    def __init__(self, pos, rate, maxParticles, particleLifetime, particleSize, particleColor, timeEmitting = -1):
        self.pos = pos
        self.rate = rate
        self.maxParticles = maxParticles
        self.particleLifetime = particleLifetime
        self.particleSize = particleSize
        self.particleColor = particleColor
        self.maxTimeEmitting = timeEmitting
        self.timeEmitting = 0
        
        self.particles = []
        
    def update(self, deltaTime):
        if self.maxTimeEmitting != -1 or self.timeEmitting < self.maxTimeEmitting:
            self.timeEmitting += deltaTime
            for particle in self.particles:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
                    
            if len(self.particles) < self.maxParticles:
                for i in range(self.rate):
                    self.particles.append(Particle(self.pos, self.particleLifetime, self.particleSize, self.particleColor))
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)