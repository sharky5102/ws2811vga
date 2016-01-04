import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math

class matrix(assembly.assembly):
    freq = 4

    class MatrixColumn(geometry.base):
        primitive = gl.GL_QUADS

        def __init__(self):
            self.head = 0.5
            self.tail = 0.2

#            maincolor = (.1, .5, .2)
            maincolors = [(.1, .1, .6), (.0, .5, .0), (.8, .0, 0)]
            maincolor = random.choice(maincolors)

            self.headcolor = (1, 1, 1, 1)
            self.color = maincolor + (.4,)
            self.pretailcolor = maincolor + (.2,)
            self.tailcolor = maincolor + (0,)

            super(matrix.MatrixColumn, self).__init__()
    
        def getVertices(self):
            verts = [(-1, -1), (+1, -1), (+1, -1+self.head), (-1, -1+self.head)]
            colors = [self.headcolor, self.headcolor, self.color, self.color]

            verts += [(-1, -1+self.head), (+1, -1+self.head), (+1, +1-self.tail), (-1, +1-self.tail)]
            colors += [self.color, self.color, self.pretailcolor, self.pretailcolor]

            verts += [(-1, +1-self.tail), (+1, +1-self.tail), (+1, +1), (-1, +1)]
            colors += [self.pretailcolor, self.pretailcolor, self.tailcolor, self.tailcolor]

            return { 'position' : verts, 'color' : colors }

    class MatrixBar:
        def __init__(self, start, slot):
            self.start = start
            self.bar = matrix.MatrixColumn()
            self.slot = slot

        def render(self, t):
            reltime = t - self.start
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, 1.5/50, .4, 1)
            transforms.translate(M, (self.slot+.5) * 2.0/50 - 1, (reltime / -5) +.6 , 0)
            self.bar.setModelView(M)
            self.bar.render()

        def setProjection(self, M):
            self.bar.setProjection(M)


    def __init__(self):
        self.slots = {}
        self.last = 0

        for i in range(0,50):
            self.slots[i] = None

    def addbar(self, t):

        slots = []
        for slot, bar in self.slots.items():
            if bar == None:
                slots.append(slot)
            elif t - bar.start > 10:
                self.slots[slot] = None

        if len(slots) == 0:
            return

        random_slot = random.choice(slots)

        self.slots[random_slot] = self.MatrixBar(t, random_slot)

    def render(self, t):
        if int(t*self.freq) > int(self.last*self.freq):
            self.addbar(t)

        self.last = t

        for slot, bar in self.slots.items():
            if not bar:
                continue
            bar.setProjection(self.projection)
            bar.render(t)

    def setProjection(self, M):
        self.projection = M


