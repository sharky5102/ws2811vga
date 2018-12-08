import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math

class stars(assembly.assembly):
    freq = 40
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
        def __init__(self, start, x, y, life, color):
            self.start = start
            self.star = stars.Star()
            self.x = x
            self.y = y
            self.life = life
            self.color = color
            self.shift = random.uniform(0,0.1)

        def render(self, t):
            reltime = t - self.start
            alpha = 1-math.fabs((self.life/2)-reltime)
            alpha *= ((1 + (math.sin((reltime + self.shift) * 20))) / 10.0) + 0.8
            self.star.color = self.color + (alpha,)
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
        while self.stars and t-self.stars[0].start > self.life:
            self.stars = self.stars[1:]

#        if len(self.stars) > 50:
#            return

        x = int(random.uniform(-25, 25))
        y = int(random.uniform(-5, 5))
        
        a = math.sin(0.11 * t * 2 * math.pi) * .3 * math.pi + math.sin(0.13 * t * 2 * math.pi) * .5 * math.pi
        l = math.sin(0.07 * t * 2 * math.pi) * 12

        mx = math.sin(a) * l
        my = math.cos(a) * l

        w = (3 - 2*abs(math.cos(0.11 * t * 2 * math.pi) * 0.6 + math.cos(0.13 * t * 2 * math.pi) * 0.3))

        x = mx + int(w*random.gauss(1, 1))
        y = my + int(w*random.gauss(1, 1))
        
        color = random.choice([(1,0.8,0.2), (1,0.9,0.7)])

        self.stars.append(stars.AnimatedStar(t, x, y, self.life, color))

    def render(self, t):
        if int(t*self.freq) > int(self.last*self.freq):
            self.addstar(t)

        self.last = t

        for star in self.stars:
            star.setProjection(self.projection)
            star.render(t)

    def setProjection(self, M):
        self.projection = M


