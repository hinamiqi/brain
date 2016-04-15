#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import numpy as np

class Actor(object):

    def __init__(self, color, start_x, start_y, width, height, enemy=False, warp = False):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.enemy = enemy
        self.warp = warp
        self.alpha = 100
        

    def _verts(self):
        verts = [self.x, self.y,
                 self.x + self.width, self.y,
                 self.x + self.width, self.y + self.height,
                 self.x, self.y + self.height]
        return verts

    def draw(self):
#         r, g, b = self.rgb_to_pyglet(self.color)
        
        pyglet.gl.glColor3f(*self.color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2f', self._verts()))
    
    def AddToBatch(self, batch):
        color = []
        for i in range(4):
            color.extend(self.color)
        self._vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None, \
                        ('v2f', self._verts()), ('c3B', color))
        
        
        
    def remove_from_batch(self, batch):
        self._vertex_list.delete()
        
        
class MovingPlatform(Actor):

    def __init__(self, color, start_x, start_y, width, height, enemy=False, warp = False):
        super().__init__(color, start_x, start_y, width, height)
        self.moving = False
        self.time = 0
        self.range = 100
        self.dx = 1
        
    def Move(self):
        if self.time >= self.range:
            self.dx = self.dx * (-1)
            self.time = 0
            
        self.x += self.dx
        self.time += 1
        
        
        
        
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
        self.invuln = False
            
    def update(self, dt):
        self.move_down(dt)
        self.move_right(dt)
        self.move_left(dt)
        self.move_up(dt)
        if self.jumping == True:
            height = self.y - self.jumppoint
            sp = height/JUMP_HEIGHT
            sp = np.cos(sp*np.pi/2)
            if sp > 0.25:
                self.up_vel += sp * 10
            else:
                self.jumppoint = self.y
                self.jumping = False
    
    def move_up(self, dt):
 
        new_y = self.y + self.up_vel 
        block = self.world.CollisionCheck2(self.x, new_y, self.width, self.height)
        if block:
            self.up_vel = 0
            self.jumping = False
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
    
    def DeathBounce(self):
        if self.up_vel > self.down_vel:
            self.up_vel += 6
        else:
            self.down_vel +=6
        if self.right_vel >= self.left_vel:
            self.left_vel += 7
        else:
            self.right_vel += 7
    
    
        


    








