import geometry
import geometry.simple
import OpenGL.GL as gl
import cv2
import cv2.cv as cv

class video(geometry.simple.texquad):
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
        
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        
        self.w = self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
        self.h = self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
        
        self.tex = gl.glGenTextures(1)
        self.n = 0
        
        super(video, self).__init__()
        

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
        if self.n == 0:
            ret, frame = self.cap.read()
            gl.glBindTexture(gl.GL_TEXTURE_RECTANGLE, self.tex)
            gl.glTexImage2D(gl.GL_TEXTURE_RECTANGLE, 0, gl.GL_RGB, self.w, self.h, 0, gl.GL_BGR, gl.GL_UNSIGNED_BYTE, frame.tostring())
            self.n = 2
        else:
            self.n -= 1
        
        
        super(video, self).render()
        