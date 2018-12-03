import assembly
import random
import geometry.simple
import OpenGL.GL as gl
import numpy as np
import transforms
import math
import pyrr

class quarters():
    def __init__(self):
        self.square = geometry.simple.square()
        
    def setProjection(self, M):
        self.projection = M

    def render(self, t):
        self.square.setProjection(self.projection)

        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, 0.0, -1, 0)
        transforms.rotate(M, t*90, 0, 0, 1)
		
        self.square.setModelView(M)
        self.square.setColor((1,1,1,1))
        self.square.render()
        
        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, -1, -1, 0)
        transforms.rotate(M, t*90, 0, 0, 1)
		
        self.square.setModelView(M)
        self.square.setColor((1,0,0,1))
        self.square.render()

        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, -1, 0, 0)
        transforms.rotate(M, t*90, 0, 0, 1)
		
        self.square.setModelView(M)
        self.square.setColor((0,1,0,1))
        self.square.render()
        M = np.eye(4, dtype=np.float32)
        transforms.translate(M, 0.0, 0, 0)
        transforms.rotate(M, t*90, 0, 0, 1)
		
        self.square.setModelView(M)
        self.square.setColor((0,0,1,1))
        self.square.render()
