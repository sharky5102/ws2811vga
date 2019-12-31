import assembly
import random
import geometry
import geometry.simple
import geometry.glyphquad
import OpenGL.GL as gl
import numpy as np
import transforms
import math
import freetype
from datetime import datetime

class newyear(assembly.assembly):
    freq = 40
    life = 2

    class Stars(geometry.base):
        primitive = gl.GL_QUADS
        dfactor = gl.GL_ONE

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
            verts = [(0, 0), (+1, 0), (+1, +1), (0, +1)]
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
            self.shift = random.uniform(0,0.1)

        def step(self, t, dt):
            self.x = self.x + self.dx * dt
            self.y = self.y + self.dy * dt
            self.dx *= 0.98
            self.dy *= 0.98

            reltime = t - self.start
            alpha = math.fabs((self.life)-reltime) 
            alpha *= ((1 + (math.sin((reltime + self.shift) * 10))) / 10.0) + 0.2
            self.color = self.basecolor + (alpha * 4,)

    def __init__(self):
        self.stars = []
        self.geometry = newyear.Stars()
        self.digits = []
        for i in range(0, 10):
            digit = geometry.glyphquad.glyphquad('./Vera.ttf', 96*64, str(i))
            digit.color = (1, 1, 1, 1)
            self.digits.append(digit)
        self.last = 0
        self.lastx = self.lasty = 0

    def addstar(self, t, dx, dy):
        while self.stars and t-self.stars[0].start > self.life:
            self.stars = self.stars[1:]

#        if len(self.stars) > 50:
#            return

        x, y = self.getCenter(t)

        w = 1

        dx += w*random.uniform(-1, 1) * 10
        dy += w*random.uniform(-1, 1) * 10
        
        color = random.choice([(1,0.8,0.2), (1,0.9,0.7)])

        self.stars.append(newyear.AnimatedStar(t, x, y, dx, dy, self.life, color))

    def getCenter(self, t): 
        a = math.sin(0.11 * t * 2 * math.pi) * .3 * math.pi + math.sin(0.13 * t * 2 * math.pi) * .5 * math.pi
        l = math.sin(0.07 * t * 2 * math.pi) * 12

        mx = math.sin(a) * l * 1.5
        my = math.cos(a) * l * 0.3

        return mx, my

    def render(self, t):
        dt = t - self.last
        x,y = self.getCenter(t)
        dx = (x - self.lastx)/dt
        dy = (y - self.lasty)/dt
        self.lastx = x
        self.lasty = y

        if int(t*self.freq) > int(self.last*self.freq):
            self.addstar(t, dx, dy)

        self.last = t

        positions = []
        colors = []
        for star in self.stars:
            star.step(t, dt)
            positions.append((star.x, star.y))
            colors.append(star.color)

        M = np.eye(4, dtype=np.float32)
        transforms.scale(M, 1.0/25, 1.0/25, 1)
        self.geometry.setStars(positions, colors)
        self.geometry.setModelView(M)
        self.geometry.render()			

        now = datetime.now()

        digits = [ now.hour / 10, now.hour % 10, now.minute / 10, now.minute % 10, now.second / 10, now.second % 10 ]
        digits = [ int(x) for x in digits ]
        
        n = 0
        for digit in digits:
            M = np.eye(4, dtype=np.float32)
            d = now.microsecond / 1000000
            s = 1.2 - d * 0.2
            transforms.scale(M, s, s, 1)
            transforms.scale(M, 1.0/12, -1.0/10, 1)
            transforms.translate(M, -.8 + (n * 0.3 ) , 0, 0)
            if n % 2 == 0:
                transforms.translate(M, 0.1 , 0, 0)
            self.digits[digit].setModelView(M)
            #self.digits[digit].color = (1,1,1, 0.5 + (1-d) * 0.5)
            self.digits[digit].render()
            n += 1

    def setProjection(self, M):
        self.projection = M


