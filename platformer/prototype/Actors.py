#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import Resources as resources
import numpy as np

#max. down_vel
GRAVITY = 10
#0-1
FLYING_MOVESPEED = 0.2
#up_vel max
JUMP_HEIGHT = 14
DEATH_BOUNCE = 10
#0-1
FRICTION = 0.5

ROLL_ANIMATION = 0.4

class Actor(object):

    def __init__(self, color, start_x, start_y, width, height, enemy=False, warp = False, type=None):
        self.type = type
        self.color = color
        self.temp_color = self.color
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.enemy = enemy
        self.warp = warp
        self.alpha = 100
        self._init()
        
    def _init(self):
        if self.type == 'dblock':
            self.enemy = True
        if self.type == 'warp':
            self.warp = True

    def _verts(self):
        verts = [self.x, self.y,
                 self.x + self.width, self.y,
                 self.x + self.width, self.y + self.height,
                 self.x, self.y + self.height]
        return verts

    def draw(self):
#         r, g, b = self.rgb_to_pyglet(self.color)
        
        pyglet.gl.glColor3f(*self.temp_color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2f', self._verts()))
    
    def AddToBatch(self, batch):
        color = []
        for i in range(4):
            color.extend(self.temp_color)
        self._vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None, \
                        ('v2f', self._verts()), ('c3B', color))
        
        
    def create_sprite(self, batch):
        self.sprite = pyglet.sprite.Sprite(resources.tiles[self.type], self.x, self.y, batch=batch)
    
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
        self.friction = FRICTION
        self.up_vel = 0
        self.down_vel = 0
        self.left_vel = 0
        self.right_vel = 0
        self.jumping = False
        self.roll_time = 0
        self.direction = 'right'
        self.moving = None
        self.rolling = False
        self.hp = 100
        self.status = 'live'
    
    def update(self, dt):
        self.velocities(dt)
        self.world.touch_check(self)
        self.move_down(dt)
        self.move_right(dt)
        self.move_left(dt)
        self.move_up(dt)
        if self.jumping:
            height = self.y - self.jumppoint
            sp = height/JUMP_HEIGHT
            sp = np.cos(sp*np.pi/2)
            if sp > 0.25:
                self.up_vel += sp * 10
            else:
                self.jumppoint = self.y
                self.jumping = False
        elif self.rolling:
            self.roll_time += dt
            #self.height = 16 
            self.temp_color = (0.7, 0.7, 0.7)
            if self.direction == 'left':
                self.left_vel = self.max_speed
            else:
                self.right_vel = self.max_speed
            if self.roll_time >= ROLL_ANIMATION:
                self.rolling = False
                self.roll_time = 0
                #self.height = 25
                self.temp_color = self.color
                
    
    def velocities(self, dt):
    
        if len(self.world.collide_d) > 0:
            self.friction = FRICTION
            for block in self.world.collide_d:
                if block.enemy:
                    self.death_bounce(dt)
                if type(block) == MovingPlatform:
                    self.x += block.dx
        else:
            self.friction = FLYING_MOVESPEED
            if self.down_vel < GRAVITY:
                self.down_vel += 0.1 * GRAVITY
            else:
                self.down_vel = GRAVITY   
        
        if self.up_vel > 0:
            self.up_vel -= 0.1 * self.max_speed
        else:
            self.up_vel = 0
            
        if self.down_vel > 0:
            self.down_vel -= 0.1 * self.max_speed 
        else:
            self.down_vel = 0

        #velocity of right direction
        if self.moving == 'right':
            if self.right_vel < self.max_speed:
                self.right_vel += 0.1 * self.max_speed * self.friction
            else:
                self.right_vel = self.max_speed * self.friction
        else:
            if self.right_vel > 0:
                self.right_vel -= 0.1 * self.max_speed * self.friction 
            else:
                self.right_vel = 0
        

        #velocity of left direction
        if self.moving == 'left':
            if self.left_vel < self.max_speed:
                self.left_vel += 0.1 * self.max_speed * self.friction
            else:
                self.left_vel = self.max_speed * self.friction
        else:
            if self.left_vel > 0:
                self.left_vel -= 0.1 * self.max_speed * self.friction
            else:
                self.left_vel = 0
    
    def move_up(self, dt):
 
        new_y = self.y + self.up_vel 
        block = self.world.collision_check(self.x, new_y, self.width, self.height)
        if block:
            self.up_vel = 0
            self.jumping = False
            self.y = block.y - self.height
        else:
            self.y += self.up_vel

    def move_down(self, dt):

        new_y = self.y - self.down_vel
        block = self.world.collision_check(self.x, new_y, self.width, self.height)
        if block:
            self.down_vel = 0
            self.up_vel = 0
            
            self.y = block.y + block.height
            
        else:
            self.y -= self.down_vel
                       
    def move_right(self, dt):

        new_x = self.x + self.right_vel 
        block = self.world.collision_check(new_x, self.y, self.width, self.height)
        if block:
            self.right_vel = 0
            self.x = block.x - self.width 
        else:
            self.x += self.right_vel
            
    def move_left(self, dt):

        new_x = self.x - self.left_vel 
        block = self.world.collision_check(new_x, self.y, self.width, self.height)
        if block:
            self.left_vel = 0
            self.x = block.x + block.width
        else:
            self.x -= self.left_vel
    
    def move_jump(self):
        if len(self.world.collide_d) > 0:
                self.jumppoint = self.y
                self.jumping = True
    
    def move_roll(self):
        if len(self.world.collide_d) > 0:
            self.rolling = True
        
    
    def death_bounce(self, dt):
        if not self.rolling:
            # if self.direction == 'left':
                # self.right_vel += 2
            # else:
                # self.left_vel += 2

            self.hp -= 1
            if self.hp <= 0:
                self.status = 'dead'
            

    
        


    








