import geometry
import math
import OpenGL.GL as gl
import numpy as np
import ctypes

class signalgenerator(geometry.base):
    vertex_code = """
        #version 120
        uniform mat4 modelview;
        uniform mat4 projection;

        attribute vec2 position;
        attribute vec2 texcoor;

        varying vec2 v_texcoor;
        
        void main()
        {
            gl_Position = projection * modelview * vec4(position,0,1);
            v_texcoor = texcoor;
        } """

    fragment_code = """
        #version 120

        uniform sampler2D tex;
        varying vec2 v_texcoor;
        
        void main()
        {
            int y = int(v_texcoor.y * 1000);
            int pixel = y / 2;
            int subpixel = int(mod(y,2));
            
            int bit = int(v_texcoor.x * 12); // 12 bits per scanline
            bit += int(subpixel * 12); // second scanline
            
            float sourcex = (float(mod(pixel,50)) + 0.5) / 50;
            float sourcey = (float(pixel / 50) + 0.5) / 10;
            
            // Reverse odd scanline sampling locations for snake trail
            if (mod((pixel / 50), 2) == 1)
                sourcex = 1 - sourcex;
                
            vec3 t = texture2D(tex, vec2(sourcex, sourcey), 3).rgb;
            
            t = pow(t, vec3(2.2));
            
            int ledvalue = int(t.r * 255);
            ledvalue = ledvalue * 256;
            ledvalue += int(t.g * 255);
            ledvalue = ledvalue * 256;
            ledvalue += int(t.b * 255);
            
            int bitvalue = int(floor(ledvalue / pow (2, 23 - bit)) - 2*floor(ledvalue / pow (2, 24 - bit)));
            
            float bitoffset = (v_texcoor.x * 12) - (mod(bit, 12));
            
            float color;
            
            if(bitvalue < 1)
                color = bitoffset < 0.1 ? 1 : 0;
            else
                color = bitoffset < 0.48 ? 1 : 0;

            gl_FragColor = vec4(color, color, color, 1);
            
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
        