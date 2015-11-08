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

        return verts, colors

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

            f_color = textureLod(tex, coor, 2);
        } """
        
    def loadGeometry(self):
        # Request a buffer slot from GPU
        buffer = gl.glGenBuffers(1)

        # Make this buffer the default one
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

        # Build data
        (verts, texcoors) = self.getVertices()
        
        if len(texcoors) != len(verts):
            raise RuntimeError('len(colors) != len(verts)')

        data = np.zeros(len(verts), [("position", np.float32, 2),
                                     ("texcoor",  np.float32, 2)])


        data['position'] = verts
        data['texcoor'] =  texcoors

        self.stride = data.strides[0]
        self.offset = ctypes.c_void_p(data.dtype["position"].itemsize)


        # Upload data
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

        return buffer, len(verts)

    def getVertices(self):
        verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
        coors = [(0, 0), (1, 0), (1, 1), (0, 1)]
        
        return verts, coors
        
    def render(self):
        # Select our shaders
        gl.glUseProgram(self.program)
        
        # Use correct modelview
        loc = gl.glGetUniformLocation(self.program, "modelview")
        gl.glUniformMatrix4fv(loc, 1, False, self.modelview)

        # Use correct projection
        loc = gl.glGetUniformLocation(self.program, "projection")
        gl.glUniformMatrix4fv(loc, 1, False, self.projection)

        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        loc = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertexBuffer)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, self.stride, ctypes.c_void_p(0))

        loc = gl.glGetAttribLocation(self.program, "texcoor")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertexBuffer)
        gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, self.stride, self.offset)

        gl.glDrawArrays(gl.GL_QUADS, 0, self.vertices)
    
    def setTexture(self, tex):
        self.tex = tex
        