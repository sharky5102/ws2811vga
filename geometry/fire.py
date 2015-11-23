import geometry
import geometry.simple
import OpenGL.GL as gl
import struct
import math
import random

class fire(geometry.simple.texquad):
    fragment_code = """
        #version 150

        uniform samplerRect tex;
        out vec4 f_color;
        in vec2 v_texcoor;
        
        void main()
        {
            float pixsize_x = 1.0/50;
            float pixsize_y = 1.0/10;
            
            vec2 coor;
            
            coor.x = (floor(v_texcoor.x/pixsize_x)+0.5)*pixsize_x;
            coor.y = (floor(v_texcoor.y/pixsize_y)+0.5)*pixsize_y;

            f_color = texture(tex, coor);
        } """
        
    def __init__(self):
        self.w = 64
        self.h = 10
        self.t = 0
        
        self.tex = gl.glGenTextures(1)
        self.n = 0
        
        super(fire, self).__init__()
        self.data = bytearray(struct.pack('BBB', 0,0,0) * (self.h+1) * self.w)

    def getVertices(self):
        verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
        coors = [(0, 0), (self.w, 0), (self.w, self.h), (0, self.h)]
        
        return { 'position' : verts, 'texcoor' : coors }

    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_RECTANGLE, self.tex)
        
        geometry.base.draw(self)
        
    def pix(self, buf, x, y, r, g, b):
        buf[y*self.w*3+x*3+0] = r
        buf[y*self.w*3+x*3+1] = g
        buf[y*self.w*3+x*3+2] = b

    def getpix(self, b, x, y):
        return b[y*self.w*3+x*3+0]
        
    def render(self):
        data = self.data
        
        for x in range(0, self.w):
            u = int(random.uniform(0, 8))
            u = 255 if u == 0 else 0
            self.pix(self.data, x, 0, u, u, u)
        
        for x in range(0,self.w):
            for y in range(1,10):
                acc = self.getpix(self.data, x-1, y-1)
                acc += self.getpix(self.data, x, y-1)
                acc += self.getpix(self.data, x+1, y-1)
                #acc += self.getpix(self.data, x+2, y-1)
                #acc += self.getpix(self.data, x-2, y-1)
                acc /= 3
                acc *= 0.9
                acc = int(acc)
                
                self.pix(data, x, y, acc, acc, acc)

        self.data = data

        gl.glBindTexture(gl.GL_TEXTURE_RECTANGLE, self.tex)
        gl.glTexImage2D(gl.GL_TEXTURE_RECTANGLE, 0, gl.GL_RGB, self.w, self.h, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, str(self.data[self.w*3:]))

        super(fire, self).render()
