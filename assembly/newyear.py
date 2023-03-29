import assembly
import random
import geometry
import geometry.simple
import OpenGL.GL as gl
import numpy as np
import transforms
import math
from datetime import datetime

class newyear(assembly.assembly):
    freq = 140
    life = 4

    class Stars(geometry.base):
        primitive = gl.GL_QUADS
        srcblend = gl.GL_SRC_ALPHA
        dstblend = gl.GL_ONE

        instanceAttributes = { 'offset' : 2, 'color' : 4 }
        attributes = { 'position' : 2 }

        vertex_code = """
            uniform mat4 modelview;
            uniform mat4 projection;
            uniform vec4 objcolor;

            in highp vec4 color;
            in highp vec2 position;
            in highp vec2 offset;
            out highp vec4 v_color;
            void main()
            {
                gl_Position = projection * modelview * vec4(position + offset,0.0,1.0);
                v_color =  objcolor * color;
            } 
        """

        def __init__(self):
            self.starcolor = (1,1,1,1)
            self.positions = []
            self.colors = []

            super(newyear.Stars, self).__init__()
    
        def getVertices(self):
            verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
            colors = [self.starcolor, self.starcolor, self.starcolor, self.starcolor]

            return { 'position' : verts, 'color' : colors }
            
        def setStars(self, positions, colors):
            self.positions = positions
            self.colors = colors
            self.reloadInstanceData()

        def getInstances(self):
            return { 'offset' : self.positions, 'color' : self.colors }

    class AnimatedStar:
        def __init__(self, start, x, y, dx, dy, life, basecolor):
            self.start = start
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.life = life
            self.basecolor = basecolor
            self.shift = random.uniform(0,1)

        def step(self, t, dt):
            self.x = self.x + self.dx * dt
            self.y = self.y + self.dy * dt
            self.dx -= (0.005 * dt * math.pow(self.dx, 3))
            self.dy -= (0.005 * dt * math.pow(self.dy, 3))

            reltime = t - self.start
            alpha = math.fabs((self.life)-reltime) 
            alpha *= ((1 + (math.sin((reltime + self.shift) * 10))) / 10.0) + 0.2
            self.color = self.basecolor + (alpha/2,)

    def __init__(self):
        self.stars = []
        self.geometry = newyear.Stars()
        self.digits = []
        #for i in range(0, 10):
        self.last = 0
        self.lastx = self.lasty = 0

    def addstar(self, t, dx, dy):
        while self.stars and t-self.stars[0].start > self.life:
            self.stars = self.stars[1:]

        x, y = self.getCenter(t)

        w = 5

        a = random.uniform(0, math.pi * 2)
        dx += w*math.cos(a)
        dy += w*math.sin(a)
        
        color = random.choice([(1,0.8,0.2), (1,0.9,0.6)])

        self.stars.append(newyear.AnimatedStar(t, x, y, dx, dy, self.life, color))

    def getCenter(self, t):
        t = t * 4
        a = math.sin(0.11 * t * 2 * math.pi) * .3 * math.pi + math.sin(0.13 * t * 2 * math.pi) * .5 * math.pi
        l = math.sin(0.07 * t * 2 * math.pi) * 12

        mx = math.sin(a) * l * 1.5
        my = math.cos(a) * l * 1.5

        return mx, my

    def render(self, t):
        dt = t - self.last
        x,y = self.getCenter(t)

        if int(t*self.freq) > int(self.last*self.freq) and dt > 0:
            dx = (x - self.lastx)/dt
            dy = (y - self.lasty)/dt

            self.addstar(t, dx, dy)

        self.lastx = x
        self.lasty = y

        self.last = t

        positions = []
        colors = []
        for star in self.stars:
            star.step(t, dt)
            positions.append((star.x, star.y))
            colors.append(star.color)

        M = np.eye(4, dtype=np.float32)
        transforms.scale(M, 1.0/50, 1.0/50, 1)
        self.geometry.setStars(positions, colors)
        self.geometry.setModelView(M)
        self.geometry.render()			

        now = datetime.now()

        digits = [ now.hour / 10, now.hour % 10, now.minute / 10, now.minute % 10, now.second / 10, now.second % 10 ]
        digits = [ int(x) for x in digits ]
        
    def setProjection(self, M):
        self.projection = M


