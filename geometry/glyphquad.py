import geometry.simple
import freetype
import OpenGL.GL as gl

class glyphquad(geometry.simple.alphatexquad):
    def __init__(self, face, size, c):
        super(glyphquad, self).__init__()
        tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        face = freetype.Face(face)
        face.set_char_size(size)
        face.load_char(c, freetype.FT_LOAD_RENDER)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, face.glyph.bitmap.pitch, face.glyph.bitmap.rows, 0, gl.GL_RED, gl.GL_UNSIGNED_BYTE, face.glyph.bitmap.buffer)
        self.setTexture(tex)
