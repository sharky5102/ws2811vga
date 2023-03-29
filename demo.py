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

import pygame

def start_music():
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load('loreen.mp3')
	pygame.mixer.music.play()

import assembly.copperbar
import assembly.circles
import assembly.snow
#import assembly.sint
import assembly.matrix
import assembly.particles
import assembly.tree
import assembly.rotate

import geometry.ws2811
import geometry.hub75e

start = time.time()
lastTime = 0

ps = []
screenWidth = 0
screenHeight = 0

def reltime():
    global start, lastTime, args

    if args.music:
         t = ((pygame.mixer.music.get_pos()-1100) / 454.3438)
    else:
        t = time.time() - start

    lastTime = t

    return t
 
def clear():   
    gl.glClearColor(0, 0, 0, 0)    
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

def display():
    global args, mainfbo, texquad, signalgenerator

    with mainfbo:
        clear()
        t = reltime()
        effect.render(t)
        
    gl.glClearColor(0, 0, 0, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT| gl.GL_DEPTH_BUFFER_BIT)

    gl.glViewport(0, 0, screenWidth, screenHeight)
    texquad.render()

    glut.glutSwapBuffers()
    glut.glutPostRedisplay()
    
def reshape(width,height):
    global screenWidth, screenHeight
    
    print( width, height )
    
    screenWidth = width
    screenHeight = height
    
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\033':
        sys.exit( )
		
    if key == b' ':
        print('%d', pygame.mixer.music.get_pos())

parser = argparse.ArgumentParser(description='Amazing WS2811 VGA driver')
parser.add_argument('--music', action='store_const', const=True, help='Sync to music')
parser.add_argument('--fullscreen', action='store_true', help='Fullscreen mode')

args = parser.parse_args()

# GLUT init
# --------------------------------------

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow(b'Amazing ws2811 VGA renderer')
glut.glutReshapeWindow(1000,1000)

glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

# Primary offscreen framebuffer
mainfbo = fbo.FBO(512, 512)

# Emulation shader
texquad = geometry.simple.texquad()
texquad.setTexture(mainfbo.getTexture())

# Projection matrix
M = np.eye(4, dtype=np.float32)
transforms.scale(M, 1, 1, 1)

# Effect
import assembly.newyear

effect = assembly.newyear.newyear()
effect.setProjection(M)

if args.music:
	start_music()

if args.fullscreen:
    glut.glutFullScreen()
glut.glutMainLoop()
