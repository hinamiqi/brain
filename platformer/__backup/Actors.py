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
        self.delta_x = 0
        self.delta_y = 0
        self.max_speed = 10
        self.up_vel = 0
        self.down_vel = 0
        self.left_vel = 0
        self.right_vel = 0
        self.collide = {'Up': False, 'Down': False, 'Left': False, 'Right': False}

    def CollisionCheck(self, block):
        if self.x + self.width >= block.x and \
            self.y + self.height >= block.y and \
            self.y <= block.y + block.height:
            self.collide['Right'] = True


        elif self.x <= block.x + block.width and \
            self.y + self.height >= block.y and \
            self.y <= block.y + block.height:
            self.collide['Left'] = True


        elif self.y + self.height >= block.y and \
            self.x + self.width >= block.x and \
            self.x <= block.x + block.width:
            self.collide['Up'] = True


        elif self.y <= block.y + block.height and \
            self.x + self.width >= block.x and \
            self.x <= block.x + block.width:
            self.collide['Down'] = True

        else:
            self.collide = {'Up': False, 'Down': False, 'Left': False, 'Right': False}


#    def Moving(self):
#        
#        if self.delta_x != 0:
#            self.x = self.x + self.delta_x
#        if self.delta_y != 0:
#            self.y = self.y + self.delta_y
    
    def move_up(self, dt):
        
        # if self.collide['Up'] == False:
            # self.y += self.up_vel * dt
            
        # res = self.world.Interaction(self)
        # if res:
            # self.up_vel = res
        self.y += self.up_vel 
        if self.world.CollisionCheck(self):
            self.y -= (self.y + self.height) - self.world.block.y

    def move_down(self, dt):
        # if self.collide['Down'] == False:
        self.y -= self.down_vel
        if self.world.CollisionCheck(self):
            self.y += (self.world.block.y + self.world.block.height) - self.y
            
    def move_right(self, dt):
        # if self.collide['Right'] == False:
        self.x += self.right_vel 
        if self.world.CollisionCheck(self):
            self.x -= (self.x + self.width) - self.world.block.x
            
    def move_left(self, dt):
        # if self.collide['Left'] == False:
        self.x -= self.left_vel 
        if self.world.CollisionCheck(self):
            self.x += (self.world.block.x + self.world.block.width) - self.x

    # def Moving(self):
        # y = self.up_vel - self.down_vel
        # x = self.right_vel - self.left_vel
        # self.x += x
        # self.y += y



















