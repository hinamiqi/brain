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
        

    def _vert(self):
        verts = [self.x, self.y,
                 self.x + self.width, self.y,
                 self.x + self.width, self.y + self.height,
                 self.x, self.y + self.height]
        return verts

    def draw(self):
#         r, g, b = self.rgb_to_pyglet(self.color)
        pyglet.gl.glColor3f(*self.color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2f', self._vert()))

class Player(Actor):
    def __init__(self, world, color, start_x, start_y, width, height):
        super().__init__(color, start_x, start_y, width, height)
        self.world = world
        self.max_speed = 7
        self.up_vel = 0
        self.down_vel = 0
        self.left_vel = 0
        self.right_vel = 0
        self.jumping = False
        self.inc = 0

            
    def move_up(self, dt):
 
        new_y = self.y + self.up_vel 
        block = self.world.CollisionCheck2(self.x, new_y, self.width, self.height)
        if block:
            self.up_vel = 0
            self.y = block.y - self.height
        else:
            self.y += self.up_vel

    def move_down(self, dt):

        new_y = self.y - self.down_vel
        block = self.world.CollisionCheck2(self.x, new_y, self.width, self.height)
        if block:
            self.down_vel = 0
            self.up_vel = 0
            
            self.y = block.y + block.height
            print('yay')
        else:
            self.y -= self.down_vel
                       
    def move_right(self, dt):

        new_x = self.x + self.right_vel 
        block = self.world.CollisionCheck2(new_x, self.y, self.width, self.height)
        if block:
            self.right_vel = 0
            self.x = block.x - self.width 
        else:
            self.x += self.right_vel
            
    def move_left(self, dt):

        new_x = self.x - self.left_vel 
        block = self.world.CollisionCheck2(new_x, self.y, self.width, self.height)
        if block:
            self.left_vel = 0
            self.x = block.x + block.width
        else:
            self.x -= self.left_vel


    








