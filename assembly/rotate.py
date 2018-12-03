import assembly
import random
import geometry.simple
import OpenGL.GL as gl
import numpy as np
import transforms
import math
import pyrr

class rotate():
    def __init__(self):
        self.square = geometry.simple.square()
        
    def setProjection(self, M):
        self.projection = M

    def renderold(self, t):
        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, -.5, 0, 0)
        transforms.rotate(M, t*360, 0, 0, 1)
        transforms.scale(M, 5, 5, 5)

        p = math.floor(t / 8)
        off = t - p * 8

        b = max(0, 1 - ((t % 1) * 4))
        m = 1 if off % 0.75 < 0.2 else 0
        d = max(0, 1 - ((t % 16) * 1))
		
		
        self.square.setProjection(self.projection)
        self.square.setModelView(M)
        self.square.setColor((b,m,d,1))
        self.square.render()
        M = np.eye(4, dtype=np.float32)

        transforms.translate(M, -.5, 0, 0)
        transforms.rotate(M, t*360+180, 0, 0, 1)
        transforms.scale(M, 5, 5, 5)

        self.square.setProjection(self.projection)
        self.square.setModelView(M)
        #self.square.setColor((.1,.1,.1,1))
        self.square.render()

    def render(self, t):
        p = math.floor(t / 8)
        off = t - p * 8

        b = max(0, 1 - ((t % 1) * 4))
        m = 1 if off % 0.75 < 0.2 else 0
        d = max(0, 1 - ((t % 16) * 1))
		

        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, 0, -.5, 0)
        #transforms.rotate(M, t*90, 0, 0, 1)
        transforms.scale(M, 5, 5, 5)

		
        self.square.setProjection(self.projection)
        self.square.setModelView(M)
        self.square.setColor((b,0,d,1))
        self.square.render()
        M = np.eye(4, dtype=np.float32)

        transforms.translate(M, -1, -.5, 0)
        #transforms.rotate(M, t*90, 0, 0, 1)
        transforms.scale(M, 5, 5, 5)

        self.square.setProjection(self.projection)
        self.square.setModelView(M)
        self.square.setColor((m,m,m,1))
        self.square.render()

