#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

class Actor(object):

    def __init__(self, color, start_x, start_y, width, height):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        

    def vert(self):
        verts = [self.x, self.y,
                 self.x + self.width, self.y,
                 self.x + self.width, self.y + self.height,
                 self.x, self.y + self.height]
        return verts

    def draw(self):
#         r, g, b = self.rgb_to_pyglet(self.color)
        pyglet.gl.glColor3f(*self.color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2f', self.vert()))

class Player(Actor):
    def __init__(self, world, color, start_x, start_y, width, height):
        super().__init__(color, start_x, start_y, width, height)
        self.world = world
        self.max_speed = 7
        self.up_vel = 0
        self.down_vel = 5
        self.left_vel = 0
        self.right_vel = 0
        self.jumping = False

        
        
      
    def move_up(self, dt):
 
        self.y += self.up_vel 
        block = self.world.CollisionCheck(self)
        if block:
            self.up_vel = 0
            self.y = block.y - self.height

    def move_down(self, dt):

        self.y -= self.down_vel
        block = self.world.CollisionCheck(self)
        if block:
            self.down_vel = 0
            self.y = block.y + block.height
                       
    def move_right(self, dt):

        self.x += self.right_vel 
        block = self.world.CollisionCheck(self)
        if block:
            self.right_vel = 0
            self.x = block.x - self.width 
            
    def move_left(self, dt):

        self.x -= self.left_vel 
        block = self.world.CollisionCheck(self)
        if block:
            self.left_vel = 0
            self.x = block.x + block.width

    
    # def move_up(self, dt):
 
        # self.y += self.up_vel 
        # block = self.world.CollisionCheck(self)
        # if block:
            # self.up_vel = 0
            # self.y -= (self.y + self.height) - block.y 

    # def move_down(self, dt):

        # self.y -= self.down_vel
        # block = self.world.CollisionCheck(self)
        # if block:
            # self.down_vel = 0
            # self.y += (block.y + block.height) - self.y
                       
    # def move_right(self, dt):

        # self.x += self.right_vel 
        # block = self.world.CollisionCheck(self)
        # if block:
            # self.right_vel = 0
            # self.x -= (self.x + self.width) - block.x
            
    # def move_left(self, dt):

        # self.x -= self.left_vel 
        # block = self.world.CollisionCheck(self)
        # if block:
            # self.left_vel = 0
            # self.x += (block.x + block.width) - self.x
















