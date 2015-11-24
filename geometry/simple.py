import geometry
import math
import OpenGL.GL as gl
import numpy as np
import ctypes

class circle(geometry.base):
    segs = 16
    
    def getVertices(self):
        colors = []
        verts = []

        for i in range(0,self.segs):
             colors.append((1,1,1,1))
             colors.append((1,1,1,1))
             colors.append((1,1,1,1))
             verts.append((0,0))
             verts.append((math.sin(math.pi*2*i/self.segs), math.cos(math.pi*2*i/self.segs)))
             verts.append((math.sin(math.pi*2*(i+1)/self.segs), math.cos(math.pi*2*(i+1)/self.segs)))

        return { 'position' : verts, 'color' : colors }

class texquad(geometry.base):
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
            float pixsize_x = 1.0/50;
            float pixsize_y = 1.0/10;
            
            vec2 coor;
            
            coor.x = (floor(v_texcoor.x/pixsize_x)+0.5)*pixsize_x;
            coor.y = (floor(v_texcoor.y/pixsize_y)+0.5)*pixsize_y;
            
            vec2 d = v_texcoor - coor;
            d.x *= 5;
            
            float p = 1-length(d)*20;
            float p2 = length(d) > 1.0 * pixsize_x ? 0.0 : 1.0;
            
            vec4 t = textureLod(tex, coor, 2);
            
            f_color = t * p + t * p2 ;
        } """
        
    attributes = { 'position' : 2, 'texcoor' : 2 }
    primitive = gl.GL_QUADS
        
    def getVertices(self):
        verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
        coors = [(0, 0), (1, 0), (1, 1), (0, 1)]
        
        return { 'position' : verts, 'texcoor' : coors }
        
    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        super(texquad, self).draw()

    def setTexture(self, tex):
        self.tex = tex

class copper(texquad):
    tex = 0
    fragment_code = """
        #version 150

        out vec4 f_color;
        in vec2 v_texcoor;
        uniform vec2 direction;
        uniform vec4 color;

        void main()
        {
            vec2 b = direction;
            vec2 a = v_texcoor;

            float c = (sin(dot(a,b) / dot(b,b)) + 1) / 2; 
            f_color = vec4(color.rgb, c);
        } """

    def getVertices(self):
        verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
        coors = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        
        return { 'position' : verts, 'texcoor' : coors }

    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "direction")
        gl.glUniform2f(loc, self.direction[0], self.direction[1])
        loc = gl.glGetUniformLocation(self.program, "color")
        gl.glUniform4f(loc, self.color[0], self.color[1], self.color[2], 1)
        
        super(copper, self).draw()
        
    def setDirection(self, v):
        self.direction = v

    def setColor(self, color):
        self.color = color
