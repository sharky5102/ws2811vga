import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math

class twinkle(assembly.assembly):
    freq = 30
    life = 1

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

            super(twinkle.Stars, self).__init__()
    
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
            self.dx *= 0.95
            self.dy *= 0.95

            reltime = (t - self.start) / self.life
            alpha = 1-math.fabs(reltime*2-1)
            alpha *= ((1 + (math.sin((reltime + self.shift) * 30))) / 10.0) + 0.45
            self.color = self.basecolor + (alpha*2 ,)

    def __init__(self):
        self.stars = []
        self.geometry = twinkle.Stars()
        self.last = 0
        self.lastx = self.lasty = 0

    def addstar(self, t, x, y):
        while self.stars and t-self.stars[0].start > self.life:
            self.stars = self.stars[1:]

        color = random.choice([(1,1,1), (0.6, 0.6, 1)])
        
        dx = dy = 0

        self.stars.append(twinkle.AnimatedStar(t, x, y, dx, dy, self.life, color))

    def render(self, t):
        dt = t - self.last

        if int(t*self.freq) > int(self.last*self.freq):
            x = int(random.uniform(-25, 25))
            y = int(random.uniform(-5, 5))
            self.addstar(t, x, y)

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

    def setProjection(self, M):
        self.projection = M


