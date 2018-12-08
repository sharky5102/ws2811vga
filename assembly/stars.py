import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math

class stars(assembly.assembly):
    freq = 10
    life = 2

    class Star(geometry.base):
        primitive = gl.GL_QUADS

        def __init__(self):
            self.starcolor = (1,1,1,1)

            super(stars.Star, self).__init__()
    
        def getVertices(self):
            verts = [(0, 0), (+1, 0), (+1, +1), (0, +1)]
            colors = [self.starcolor, self.starcolor, self.starcolor, self.starcolor]

            return { 'position' : verts, 'color' : colors }

    class AnimatedStar:
        def __init__(self, start, x, y, life):
            self.start = start
            self.star = stars.Star()
            self.x = x
            self.y = y
            self.life = life

        def render(self, t):
            reltime = t - self.start
            self.star.color = (1,1,1,1-math.fabs((self.life/2)-reltime))
            M = np.eye(4, dtype=np.float32)
            transforms.translate(M, self.x, self.y , 0)
            transforms.scale(M, 1.0/25, 1.0/25, 1)
            self.star.setModelView(M)
            self.star.render()

        def setProjection(self, M):
            self.star.setProjection(M)


    def __init__(self):
        self.stars = []
        self.last = 0

    def addstar(self, t):
        if self.stars and t-self.stars[0].start > self.life:
            self.stars = self.stars[1:]

        if len(self.stars) > 50:
            return

        self.stars.append(stars.AnimatedStar(t, int(random.uniform(-25, 25)), int(random.uniform(-5, 5)), self.life))

    def render(self, t):
        if int(t*self.freq) > int(self.last*self.freq):
            self.addstar(t)

        self.last = t

        for star in self.stars:
            star.setProjection(self.projection)
            star.render(t)

    def setProjection(self, M):
        self.projection = M


