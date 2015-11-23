import geometry
import math
import OpenGL.GL as gl
import numpy as np
import ctypes

class signalgenerator(geometry.base):
    vertex_code = """
        #version 150
        uniform mat4 modelview;
        uniform mat4 projection;
        
        in vec2 position;
        in vec2 texcoor;

        out vec2 v_texcoor;
        
        void main()
        {
            gl_Position = projection * modelview * vec4(position,0,1);
            v_texcoor = texcoor;
        } """

    fragment_code = """
        #version 150

        uniform sampler2D tex;
        out vec4 f_color;
        in vec2 v_texcoor;
        
        void main()
        {
            int y = int(v_texcoor.y * 1000);
            int pixel = y / 2;
            int subpixel = y % 2;
            
            int bit = int(v_texcoor.x * 12); // 12 bits per scanline
            bit += int(subpixel * 12); // second scanline
            
            float sourcex = (float(pixel % 50) + 0.5) / 50;
            float sourcey = (float(pixel / 50) + 0.5) / 10;
            
            // Reverse odd scanline sampling locations for snake trail
            if ((pixel / 50) % 2 == 1)
                sourcex = 1 - sourcex;
                
            vec4 t = textureLod(tex, vec2(sourcex, sourcey), 2);
            
            int ledvalue = int(t.r * 255);
            ledvalue = ledvalue << 8;
            ledvalue |= int(t.g * 255);
            ledvalue = ledvalue << 8;
            ledvalue |= int(t.b * 255);
            
            int bitvalue = (ledvalue >> (23 - bit)) & 1;
            
            float bitoffset = (v_texcoor.x * 12) - (bit % 12);
            
            float color;
            
            if(bitvalue == 0)
                color = bitoffset < 0.1 ? 1 : 0;
            else
                color = bitoffset < 0.48 ? 1 : 0;

            f_color = vec4(color, color, color, 3);
            
        } """
        
    attributes = { 'position' : 2, 'texcoor' : 2 }
    primitive = gl.GL_QUADS
        
    def getVertices(self):
        verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
        coors = [(0, 1), (1, 1), (1, 0), (0, 0)]
        
        return { 'position' : verts, 'texcoor' : coors }
        
    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        super(signalgenerator, self).draw()

    def setTexture(self, tex):
        self.tex = tex
        