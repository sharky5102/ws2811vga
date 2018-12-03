import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math

class particles():
    freq = .5
    maxparts = 3
        
    def __init__(self):
        self.last = 0
        self.ps = []

    def setProjection(self, M):
        self.projection = M

    def render(self, t):
        if int(t*self.freq) > int(self.last*self.freq):
            p = particle((random.uniform(-1, 1), random.uniform(-1, 1)), t)
            p.setProjection(self.projection)
            self.ps.append(p)
        self.last = t

        if len(self.ps) >= self.maxparts:
            self.ps = self.ps[1:]
        
        for p in self.ps:
            p.render(t)

class particle(assembly.assembly):
    class Particle:
        def __init__(self, pos, v, m):
            self.pos = pos
            self.v = v
            self.part = geometry.simple.circle()
            self.part.setColor((1,.5,0,.5))
            self.m = m
            self.flicker = random.uniform(2, 2.5)
                
        def step(self, dt):
            self.pos = (self.pos[0] + self.v[0] * dt, self.pos[1] + self.v[1] * dt)
            self.v = (self.v[0] * math.pow(0.1 * self.m, dt * 2), self.v[1] * math.pow(0.1 * self.m, dt * 2) - 0.002)

        def render(self, t):
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, .03 * self.m, .03 * self.m, 1)
            transforms.translate(M, self.pos[0], self.pos[1], 0)
            
            if t > self.flicker:
                dt = t - self.flicker

                a = max(0, .5 - math.pow(dt/4, 2))

                n = math.sin(dt*30)/2 + 0.5
                self.part.setColor((1,.5 + n * .5, n, a))

            self.part.setModelView(M)
            self.part.render()

        def setProjection(self, p):
            self.part.setProjection(p)

    def __init__(self, spos, start):
        self.particles = []
        self.last = None
        self.start = start

        for i in range(0, 50):
            pos = (spos[0] + random.uniform(-.01, .01), spos[1] + random.uniform(-.01, .01))
            a = random.uniform(0, 2 * math.pi)
            v = (1.0 * math.sin(a) * random.uniform(1.0, 1.5), 1.0 * math.cos(a) * random.uniform(1.0, 1.5))
            m = random.uniform(0.8, 1.2)
            self.particles.append(self.Particle(pos, v, m))

    def step(self, dt):
        for p in self.particles:
            p.step(dt)

    def render(self, t):
        if self.last:
            self.step(t - self.last);
        self.last = t

        for p in self.particles:
            p.setProjection(self.projection)
            p.render(t - self.start);

    def setProjection(self, p):
        self.projection = p