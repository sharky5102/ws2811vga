import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms

class matrix(assembly.assembly):
    class MatrixColumn(geometry.base):
        primitive = gl.GL_QUADS

        def __init__(self):
            self.head = 0.2
            self.tail = 0.2
            self.headcolor = (.5, 1, .5, 1)
            self.color = (0, .5, 0, 1)
            self.tailcolor = (0, .5, 0, 0)

            super(matrix.MatrixColumn, self).__init__()
    
        def getVertices(self):
            verts = [(-1, -1), (+1, -1), (+1, -1+self.head), (-1, -1+self.head)]
            colors = [self.headcolor, self.headcolor, self.color, self.color]

            verts += [(-1, -1+self.head), (+1, -1+self.head), (+1, +1-self.tail), (-1, +1-self.tail)]
            colors += [self.color, self.color, self.color, self.color]

            verts += [(-1, +1-self.tail), (+1, +1-self.tail), (+1, +1), (-1, +1)]
            colors += [self.color, self.color, self.tailcolor, self.tailcolor]

            return { 'position' : verts, 'color' : colors }

    class MatrixBar:
        def __init__(self, start, slot):
            self.start = start
            self.bar = matrix.MatrixColumn()
            self.slot = slot

        def render(self, t):
            reltime = t - self.start
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, 1.0/50, 0.4, 1)
            transforms.translate(M, (self.slot+.5) * 2.0/50 - 1, (reltime / -10) +.6 , 0)
            self.bar.setModelView(M)
            self.bar.render()

        def setProjection(self, M):
            self.bar.setProjection(M)


    def __init__(self):
        self.slots = {}

        for i in range(0,50):
            self.slots[i] = None

    def addbar(self, t):

        slots = []
        for slot, bar in self.slots.items():
            if bar == None:
                slots.append(slot)
            elif t - bar.start > 20:
                self.slots[slot] = None

        if len(slots) == 0:
            return

        random_slot = random.choice(slots)

        self.slots[random_slot] = self.MatrixBar(t, random_slot)

    def render(self, t):
        for slot, bar in self.slots.items():
            if not bar:
                continue
            bar.setProjection(self.projection)
            bar.render(t)

    def setProjection(self, M):
        self.projection = M


