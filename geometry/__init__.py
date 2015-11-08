import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import math
import transforms
import ctypes

class base:
    """Base class for 2d geometries with modelview and projection transforms"""    
    
    vertex_code = """
        #version 120
        uniform mat4 modelview;
        uniform mat4 projection;
        attribute vec4 color;
        attribute vec2 position;
        varying vec4 v_color;
        void main()
        {
            gl_Position = projection * modelview * vec4(position,0,1);
            v_color = color;
        } """

    fragment_code = """
        varying vec4 v_color;
        void main()
        {
            gl_FragColor = vec4(1,1,1,1) + v_color;
        } """

    def __init__(self):
        self.program = self.loadShaderProgram();
        identity = np.eye(4, dtype=np.float32)
        self.setModelView(identity);
        self.setProjection(identity);
        (self.vertexBuffer, self.vertices) = self.loadGeometry();

    def getVertices(self):
        """Override for useful geometry"""
        return ([], [])
        
    def loadShaderProgram(self):
        # Request a program and shader slots from GPU
        program  = gl.glCreateProgram()
        vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        # Set shaders source
        gl.glShaderSource(vertex, self.vertex_code)
        gl.glShaderSource(fragment, self.fragment_code)

        # Compile shaders
        gl.glCompileShader(vertex)
        gl.glCompileShader(fragment)
        print 'Vertex shader'
        print gl.glGetShaderInfoLog(vertex)
        print 'Fragment shader'
        print gl.glGetShaderInfoLog(fragment)

        # Attach shader objects to the program
        gl.glAttachShader(program, vertex)
        gl.glAttachShader(program, fragment)

        # Build program
        gl.glLinkProgram(program)

        # Get rid of shaders (no more needed)
        gl.glDetachShader(program, vertex)
        gl.glDetachShader(program, fragment)

        return program
        
    def loadGeometry(self):
        # Request a buffer slot from GPU
        buffer = gl.glGenBuffers(1)

        # Make this buffer the default one
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

        # Build data
        (verts, colors) = self.getVertices()
        
        if len(colors) != len(verts):
            raise RuntimeError('len(colors) != len(verts)')

        data = np.zeros(len(verts), [("position", np.float32, 2),
                                     ("color",    np.float32, 4)])


        data['color']    = colors
        data['position'] = verts

        self.stride = data.strides[0]
        self.offset = ctypes.c_void_p(data.dtype["position"].itemsize)
        

        # Upload data
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

        return buffer, len(verts)
    
    def setModelView(self, M):
        self.modelview = M
    
    def setProjection(self, M):
        self.projection = M
    
    def render(self):
        # Select our shaders
        gl.glUseProgram(self.program)
        
        # Use correct modelview
        loc = gl.glGetUniformLocation(self.program, "modelview")
        gl.glUniformMatrix4fv(loc, 1, False, self.modelview)

        # Use correct projection
        loc = gl.glGetUniformLocation(self.program, "projection")
        gl.glUniformMatrix4fv(loc, 1, False, self.projection)

        loc = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertexBuffer)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, self.stride, ctypes.c_void_p(0))

        loc = gl.glGetAttribLocation(self.program, "color")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertexBuffer)
        gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, self.stride, self.offset)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertices)
