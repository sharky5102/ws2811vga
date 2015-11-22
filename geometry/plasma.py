import geometry
import geometry.simple
import OpenGL.GL as gl
import struct
import math

class plasma(geometry.simple.texquad):
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
        
        super(plasma, self).__init__()

    def getVertices(self):
        verts = [(-1, +1), (+1, +1), (+1, -1), (-1, -1)]
        coors = [(0, 0), (self.w, 0), (self.w, self.h), (0, self.h)]
        
        return { 'position' : verts, 'texcoor' : coors }

    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_RECTANGLE, self.tex)
        
        geometry.base.draw(self)
        
    def render(self):
        self.t += .5
        
        data = bytearray(struct.pack('BBB', 255, 255, 255) * 10 * self.w)
        
        for x in range(0,self.w):
            for y in range(0,10):
                r = math.sin(self.t * math.pi * 2 / 7 + x * math.pi * 2 / 63 + y * math.pi * 2 / 13) * 127 + 128
                g = math.sin(self.t * math.pi * 2 / 5 + x * math.pi * 2 / 43 + y * math.pi * 2 / 11) * 127 + 128
                b = math.sin(self.t * math.pi * 2 / 13 + x * math.pi * 2 / 51 +y * math.pi * 2 / 9) * 127 + 128
                
                data[y*self.w*3+x*3+0] = struct.pack('B', r)
                data[y*self.w*3+x*3+1] = struct.pack('B', g)
                data[y*self.w*3+x*3+2] = struct.pack('B', b)

        gl.glBindTexture(gl.GL_TEXTURE_RECTANGLE, self.tex)
        gl.glTexImage2D(gl.GL_TEXTURE_RECTANGLE, 0, gl.GL_RGB, self.w, self.h, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, str(data))

        super(plasma, self).render()
