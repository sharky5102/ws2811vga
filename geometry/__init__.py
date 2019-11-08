﻿import numpy as np
import OpenGL.GL as gl
import math
import transforms
import ctypes

cache = {}

class base(object):
    """Base class for 2d geometries with modelview and projection transforms"""    
    
    version = """#version 300 es\n"""
    
    vertex_code = """
        uniform mat4 modelview;
        uniform mat4 projection;
        uniform vec4 objcolor;

        in highp vec4 color;
        in highp vec2 position;
        out highp vec4 v_color;
        void main()
        {
            gl_Position = projection * modelview * vec4(position,0.0,1.0);
            v_color =  objcolor * color;
        } """

    fragment_code = """
        in highp vec4 v_color;
        out highp vec4 f_color;

        void main()
        {
            f_color = v_color;
        } """

    attributes = { 'color' : 4, 'position' : 2 }
    primitive = gl.GL_TRIANGLES

    program = None

    def __init__(self):
        global cache

        # Cache the program based on the class name
        if self.__class__.__name__ in cache:
            self.program = cache[self.__class__.__name__]
        else:
            self.program = self.loadShaderProgram()
            cache[self.__class__.__name__] = self.program

        identity = np.eye(4, dtype=np.float32)
        self.setModelView(identity);
        self.setProjection(identity);
        (self.vertexBuffer, self.vertices) = self.loadGeometry();
        self.color = (1,1,1,1)

    def __del__(self):
        gl.glDeleteBuffers(1, [self.vertexBuffer])

    def getVertices(self):
        """Override for useful geometry"""
        return ([], [])
        
    def loadShaderProgram(self):
        # Request a program and shader slots from GPU
        program  = gl.glCreateProgram()
        vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        # Set shaders source
        gl.glShaderSource(vertex, self.version + self.vertex_code)
        gl.glShaderSource(fragment, self.version + self.fragment_code)

        # Compile shaders
        gl.glCompileShader(vertex)
        gl.glCompileShader(fragment)
        log = gl.glGetShaderInfoLog(vertex)
        if log:
            print('Vertex shader')
            print(self.vertex_code)
            print(log.decode('ascii'))
            raise RuntimeError('Shader compiliation failed')
        log = gl.glGetShaderInfoLog(fragment)
        if log:
            print('Fragment shader')
            print(self.fragment_code)
            print(log.decode('ascii'))
            raise RuntimeError('Shader compiliation failed')

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
        verts = self.getVertices()
        
        size = None
        for attrib in verts:
            if size == None:
                size = len(verts[attrib]) 
                continue
            if size != len(verts[attrib]):
                raise RuntimeError('not all attribute arrays have the same length')

        format = []
        for attrib in self.attributes:
            format.append( (attrib, np.float32, self.attributes[attrib]) )

        data = np.zeros(size, format)

        offset = 0
        self.offsets = {}
        for attrib in self.attributes:
            data[attrib] = verts[attrib]
            self.offsets[attrib] = ctypes.c_void_p(offset)
            offset += data.dtype[attrib].itemsize

        self.stride = data.strides[0]

        # Upload data
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

        return buffer, size
    
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

        # Use correct color
        loc = gl.glGetUniformLocation(self.program, "objcolor")
        gl.glUniform4fv(loc, 1, self.color)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

        for attrib in self.attributes:
            loc = gl.glGetAttribLocation(self.program, attrib)
            if loc < 0:
                raise RuntimeError('Attribute %s not found in program' % attrib)
            gl.glEnableVertexAttribArray(loc)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertexBuffer)
            gl.glVertexAttribPointer(loc, self.attributes[attrib], gl.GL_FLOAT, False, self.stride, self.offsets[attrib])

        self.draw()
        
    def draw(self):
        
        gl.glDrawArrays(self.primitive, 0, self.vertices)
