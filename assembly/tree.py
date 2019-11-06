import assembly
import random
import geometry.tree
import OpenGL.GL as gl
import numpy as np
import transforms
import math
import pyrr

class tree():
    def __init__(self):
        f = open('tree.json', 'rt')
        data = f.read()
        self.tree = geometry.tree.tree(data)
        
    def setProjection(self, M):
        self.projection = M

    def render(self, t):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        M = np.eye(4, dtype=np.float32)
        transforms.rotate(M, t*4, 0, 0, 1)
        transforms.rotate(M, 80, 1, 0, 0)
        transforms.scale(M, .5, -1, .5)
        transforms.translate(M, 0, -.5, -8)

        transforms.rotate(M, 00, 1, 0, 0)
        transforms.scale(M, .5, -.5, .5)
        transforms.translate(M, 0, 0, -10)

        projection = pyrr.matrix44.create_perspective_projection(10, 1, 0.00001, 10000)
        self.tree.setProjection(projection)
        self.tree.setModelView(M)
        self.tree.render()
        gl.glDisable(gl.GL_DEPTH_TEST)

    def setTexture(self, tex):
        self.tree.setTexture(tex)