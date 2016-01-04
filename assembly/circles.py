import assembly
import geometry.simple
import numpy as np
import transforms
import random
import math
import colorsys

class circles(assembly.assembly):
    freq = 4    
    class circle(object):
        def __init__(self, pos, reltime, color):
            self.pos = pos
            self.geometry = geometry.simple.circle()
            self.reltime = reltime
            self.origcolor = color

        def update(self, t):
            self.size = math.pow(t, 0.3)/4;
            self.color = self.origcolor + (1/(math.pow(t*2,1.5)+1), )

        def render(self, t):
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
        self.circles = []
        self.time = None
        self.last = 0
        ncolors = 2
        basehue = random.uniform(0, 1)

        self.colors = [colorsys.hsv_to_rgb(basehue + float(i)/ncolors, 1, 1) for i in range(0,ncolors)]

    def addCircle(self):
        if not self.time:
            return
        c = self.circle((random.uniform(-1, 1), random.uniform(0, 0.4)-0.2), self.time, random.choice(self.colors))
        self.circles.append(c)

    def render(self, t):
        if int(t*self.freq) > int(self.last*self.freq):
            self.addCircle()

        self.last = t

        self.time = t
        for c in self.circles:
            c.setProjection(self.projection)
            c.render(t)

        self.circles = [circle for circle in self.circles if t - circle.reltime < 5]

    def setProjection(self, M):
        self.projection = M