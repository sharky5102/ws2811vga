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

start = time.time()
lastTime = 0

ps = []
screenWidth = 0
screenHeight = 0

def reltime():
    global start, lastTime, args

    if args.music:
#        t = ((pygame.mixer.music.get_pos()-1157) / 454.3438) 
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
        
    if args.emulate:
        gl.glClearColor(0, 0, 0, 0)    
        gl.glClear(gl.GL_COLOR_BUFFER_BIT| gl.GL_DEPTH_BUFFER_BIT)
        
        gl.glViewport(0, 0, int(screenWidth/2), screenHeight)
        tree.render(reltime())
        
        gl.glViewport(int(screenWidth/2), 0, int(screenWidth/2), screenHeight)
        texquad.render()
        
    else:
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        if args.preview:   
            texquad.render()
        else:
            signalgenerator.render()
                
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
parser.add_argument('--emulate', action='store_const', const=True, help='Emulate tree')
parser.add_argument('--preview', action='store_const', const=True, help='Preview windows instead of actual output')
parser.add_argument('--raw', action='store_const', const=True, help='Raw mode - use with --preview to view raw pixel data')
parser.add_argument('--music', action='store_const', const=True, help='Sync to music')
parser.add_argument('effect', help='Effect to use')

args = parser.parse_args()

# GLUT init
# --------------------------------------

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow(b'Amazing ws2811 VGA renderer')
if args.preview or args.raw:
    glut.glutReshapeWindow(1500,300)
elif args.emulate:
    glut.glutReshapeWindow(1000, 500)
else:
    glut.glutReshapeWindow(840,1000)

glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

# Primary offscreen framebuffer
mainfbo = fbo.FBO(512, 512)

# WS2811 output shader
layoutfile = 'layout.json'
signalgenerator = geometry.ws2811.signalgenerator(layoutfile)
signalgenerator.setTexture(mainfbo.getTexture())

# Emulation shader
texquad = geometry.simple.texquad()
texquad.setTexture(mainfbo.getTexture())

# Tree emulator
tree = assembly.tree.tree(layoutfile)
tree.setTexture(mainfbo.getTexture())

# Projection matrix
M = np.eye(4, dtype=np.float32)
transforms.scale(M, 1, 1, 1)

# Effect
try:
    i = __import__('assembly.%s' % args.effect)

    effect = getattr(getattr(i, args.effect), args.effect)()
    effect.setProjection(M)
except ImportError:
    print('Unable to initialize effect %s' % args.effect)
    raise

if args.music:
	start_music()

if not args.raw and not args.preview and not args.emulate:
    glut.glutFullScreen()
glut.glutMainLoop()
