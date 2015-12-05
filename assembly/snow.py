import assembly
import geometry.simple
import numpy as np
import transforms
import random
import math
import colorsys

class snow(assembly.assembly):
    class flake(object):
        def __init__(self, geometry, pos, size, reltime, color):
            self.pos = pos
            self.size = size * 2
            self.reltime = reltime
            self.v = (0, -.5 / (size/0.01))
            self.geometry = geometry
            self.laststep = reltime
            self.phase = random.uniform(0, math.pi*2)
            self.color = color

        def step(self, t):
            d = t - self.laststep
            self.laststep = t
            self.pos = (self.pos[0] + self.v[0] * d, self.pos[1] + self.v[1] * d)

        def render(self, t):
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, self.size, self.size, 1)
            transforms.translate(M, self.pos[0], self.pos[1])
            transforms.translate(M, math.sin(t * math.pi * 2 / 2 + self.phase) * 0.008 , 0)
            self.geometry.setModelView(M)
            self.geometry.setProjection(self.projection)
            self.geometry.setColor(self.color)
            self.geometry.render()

        def setProjection(self, M):
            self.projection = M

    def __init__(self):
        self.flakes = []
        self.time = None
        self.geometry = geometry.simple.circle()

    def addFlake(self):
        colors = [(1,1,1,.2), (1,1,1,.2), (1,1,1,.2), (1,1,1,.2), (1,1,1,.2), (1,.5,0,.2)]
        if not self.time:
            return

        c = self.flake(self.geometry, (random.uniform(0,4)-2, .3), random.uniform(0, 0.03) + 0.02, self.time, random.choice(colors))

        self.flakes.append(c)

    def render(self, t):
        self.time = t
        for c in self.flakes:
            c.setProjection(self.projection)
            c.render(t)

        self.flakes = [circle for circle in self.flakes if t - circle.reltime < 5]

    def setProjection(self, M):
        self.projection = M

    def step(self, t):
        for flake in self.flakes:
            flake.step(t)