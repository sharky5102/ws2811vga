import geometry
import geometry.simple
import OpenGL.GL as gl
import cv2

class video(geometry.simple.texquad):
    fragment_code = """
        uniform sampler2D tex;
        out highp vec4 f_color;
        in highp vec2 v_texcoor;
        
        void main()
        {
            highp ivec2 coor;
            
            coor.x = int(v_texcoor.x);
            coor.y = int(v_texcoor.y);

            f_color = texelFetch(tex, coor, 0);
        } """
        
    def __init__(self):
        self.filename = 'frozen.mp4'
        self.cap = cv2.VideoCapture(self.filename)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame = 0
        self.w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.tex = gl.glGenTextures(1)
        self.n = 0
        self.lastttime = 0
        
        super(video, self).__init__()
        

    def getVertices(self):
        aspect = float(self.h)/float(self.w)
        verts = [(-1, +aspect), (+1, +aspect), (+1, -aspect), (-1, -aspect)]
        coors = [(self.w, 0), (0, 0), (0, self.h), (self.w, self.h)]
        
        return { 'position' : verts, 'texcoor' : coors }

    def draw(self):
        loc = gl.glGetUniformLocation(self.program, "tex")
        gl.glUniform1i(loc, 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
        
        geometry.base.draw(self)
        
    def render(self, t):
        while self.frame / self.fps < t:
            ret, frame = self.cap.read()
                
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
            data = frame.tostring()
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.w, self.h, 0, gl.GL_BGR, gl.GL_UNSIGNED_BYTE, data)
            self.frame += 1

        super(video, self).render()
