#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 1014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import math
import transforms
import time
import fbo
import random
import argparse

import assembly.copperbar
import assembly.circles
import assembly.snow
import assembly.sint
import assembly.matrix
import assembly.particles

import geometry.ws2811

start = time.time()
lastTime = 0

ps = []

def render():
    global start, lastTime, args, effect
    
    t = time.time() - start

    lastTime = t

    gl.glClearColor(0, 0, 0, 0)    
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

    effect.render(t)

def display():
    global args, mainfbo, texquad, signalgenerator
    
    if args.raw:
        render()
    else:
        with mainfbo:
            render()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        if args.preview:   
            texquad.render()
        else:
            signalgenerator.render()
                
    glut.glutSwapBuffers()
    glut.glutPostRedisplay()
    
def reshape(width,height):
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )

parser = argparse.ArgumentParser(description='Amazing WS2811 VGA driver')
parser.add_argument('--preview', action='store_const', const=True, help='Preview windows instead of actual output')
parser.add_argument('--raw', action='store_const', const=True, help='Raw mode - use with --preview to view raw pixel data')
parser.add_argument('effect', help='Effect to use')

args = parser.parse_args()

# GLUT init
# --------------------------------------

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Amazing ws2811 VGA renderer')
if args.preview or args.raw:
    glut.glutReshapeWindow(1500,300)
else:
    glut.glutReshapeWindow(840,1000)

glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

# Primary offscreen framebuffer
mainfbo = fbo.FBO(512, 128)

# WS2811 output shader
signalgenerator = geometry.ws2811.signalgenerator()
signalgenerator.setTexture(mainfbo.getTexture())

# Emulation shader
texquad = geometry.simple.texquad()
texquad.setTexture(mainfbo.getTexture())

# Projection matrix
M = np.eye(4, dtype=np.float32)
transforms.scale(M, 1, 5, 1)

# Effect
try:
    i = __import__('assembly.%s' % args.effect)

    effect = getattr(getattr(i, args.effect), args.effect)()
    effect.setProjection(M)
except ImportError:
    print 'Unable to initialize effect %s' % args.effect
    raise

if not args.raw and not args.preview:
    glut.glutFullScreen()
glut.glutMainLoop()
