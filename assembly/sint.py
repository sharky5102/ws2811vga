import geometry.simple
import assembly
import numpy as np
import transforms

class sint(assembly.assembly):
    def __init__(self):
        self.img = geometry.simple.imgquad('sint.bmp')

    def setProjection(self, P):
        self.projection = P

    def render(self, t):
        self.img.setProjection(self.projection)

        for i in range(0,4):
            M = np.eye(4, dtype=np.float32)
            transforms.translate(M, i*2-3, 0)        
            transforms.scale(M, 1, -1)        
            transforms.scale(M, .25, .25)        
            self.img.setModelView(M)
            self.img.render()
