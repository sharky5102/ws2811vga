import assembly
import geometry.simple
import numpy as np
import transforms
import random
import math
import colorsys

class lr(assembly.assembly):
    freq = 4    
    class circle(object):
        def __init__(self, pos, reltime, color):
            self.pos = pos
            self.geometry = geometry.simple.circle()
            self.reltime = reltime
            self.origcolor = color

        def update(self, t):
            self.size = math.pow(t, 0.3)/4;
            self.color = self.origcolor + (1, )

        def render(self, t):
            self.pos = (math.cos(t) * 1, 0)
            self.update(t - self.reltime)
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, self.size, self.size, 1)
            transforms.translate(M, self.pos[0], self.pos[1])

            self.geometry.setColor(self.color)
            self.geometry.setModelView(M)
            self.geometry.setProjection(self.projection)
            self.geometry.render()

        def setProjection(self, M):
            self.projection = M

    def __init__(self):
        self.geom = self.circle((0,0), 0, (1,1,1))

    def render(self, t):
        self.geom.setProjection(self.projection)
        self.geom.render(t)

    def setProjection(self, M):
        self.projection = M