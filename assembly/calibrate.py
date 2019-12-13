import assembly
import random
import geometry
import OpenGL.GL as gl
import numpy as np
import transforms
import math
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

quit = False

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if self.path.startswith('/lamp/'):
            lampn = int(self.path[6:])
            self.server.renderer.enableLamp(lampn)

def server(renderer):
    global quit

    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HTTPHandler)    
    httpd.renderer = renderer
    
    while not quit:
        httpd.handle_request()

class calibrate(assembly.assembly):
    class Star(geometry.base):
        primitive = gl.GL_QUADS
        dfactor = gl.GL_ONE

        def __init__(self):
            self.starcolor = (1,1,1,1)

            super(calibrate.Star, self).__init__()
    
        def getVertices(self):
            verts = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
            colors = [self.starcolor, self.starcolor, self.starcolor, self.starcolor]

            return { 'position' : verts, 'color' : colors }

    def __init__(self):
        filename = 'layout.json'
        f = open(filename, 'rt')
        data = f.read()
        self.lamps = json.loads(data)
        self.star = calibrate.Star()
        self.star.color = (1,1,1,1)
        self.serverThread = threading.Thread(target=server, args=(self,))
        self.serverThread.daemon = True
        self.serverThread.start()
        self.enabledLamp = None
        
    def __destroy__(self):
        global quit
        quit = True
        self.serverThread.join()

    def render(self, t):
        n = 0
        d = (t * 10) % len(self.lamps)
        for p in self.lamps:
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, 1.0/60, 1.0/60, 1)
            transforms.translate(M, p[0], p[1], 0)
            self.star.setModelView(M)
            M = np.eye(4, dtype=np.float32)
            transforms.scale(M, 1, 1, 1)
            self.star.setProjection(M)
            if self.enabledLamp is not None:
                self.star.color = (1,1,1,1) if n == self.enabledLamp else (.1, 0, 0, 1)
            else:
                self.star.color = (1,1,1,1) if int(d) == n else (.1, 0, 0, 1)
            self.star.render()
            n+=1

    def enableLamp(self, n):
        self.enabledLamp = n

    def setProjection(self, M):
        self.projection = M


