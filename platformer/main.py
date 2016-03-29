#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.window import key
from pyglet import clock
from pyglet.gl import *

class Actor(object):
    def __init__(self, color, start_x, start_y, width, height):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.speed = 50
        self.vel = 0
        self.msg = ""

    def vert(self):
        verts = [self.x, self.y,
                 self.x + self.width, self.y,
                 self.x + self.width, self.y + self.height,
                 self.x, self.y + self.height]
        return verts

    def draw(self):
#        r, g, b = self.rgb_to_pyglet(self.color)
        glColor3f(*self.color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2i', self.vert()))

    def CollisionCheck(self, block):
        if self.x + self.width == block.x and \
            self.y + self.height > block.y and \
            self.y < block.y + block.height:
            self.msg = "Right!"
            return True

        elif self.x == block.x + block.width and \
            self.y + self.height > block.y and \
            self.y < block.y + block.height:
            self.msg = "Left!"
            return True

        elif self.y + self.height == block.y and \
            self.x + self.width > block.x and \
            self.x < block.x + block.width:
            self.msg = "Top!"
            return True

        elif self.y == block.y + block.height and \
            self.x + self.width > block.x and \
            self.x < block.x + block.width:
            self.msg = "Bot!"
            return True
        else:
            self.msg = ""


    def update(self):
        pass


def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result[0], result[1], result[2]

class App(pyglet.window.Window):

    def __init__(self, color):
        pyglet.window.Window.__init__(self, 512, 480)
        self.color = color
        
        clock.set_fps_limit(60)
        
    def on_draw(self):
        glClearColor(*self.color, 1)
        
        self.clear()
        
    def mainLoop(self):
        pyglet.app.run()
            
            #self.draw()


























