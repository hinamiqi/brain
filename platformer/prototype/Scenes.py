#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import os
import numpy as np

from pyglet.gl import *

from Physics import *
from MapLoader import *
from Rules import *

RED = (250, 0, 0, 255)
WHITE = (250, 250, 250, 255)

UNSELECTED = (184, 134, 11, 255)
SELECTED = (190, 34, 35, 255)

SKY = (176, 224, 230, 255)
PLAYER = (107, 142, 35)
GROUND = (184, 134, 11)
LAVA = (227, 38, 54)
WARP = (102, 204, 102)

#max. down_vel
GRAVITY = 10
#0-1
FLYING_MOVESPEED = 0.2
#up_vel max
JUMP_HEIGHT = 14
DEATH_BOUNCE = 10
#0-1
FRICTION = 0.5
INERTION = 1.3

#normalize 0-255 to 0-1
def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result


class TitleScreen(object):
    
    def __init__(self, width, height):
        self.win_w = width
        self.win_h = height
        self.BCKND_COLOR = [0, 0, 0, 1]
        self.END = False

        self.batch = pyglet.graphics.Batch()
        self._init()
        
    def _init(self):
        self.title = pyglet.text.Label('PROTOTYPE', anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=62, color=UNSELECTED, batch=self.batch, x=self.win_w//2, y=self.win_h*0.6)
        self.main_label = pyglet.text.Label('press start', anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=22, color=WHITE, batch=self.batch, x=self.win_w//2, y=self.win_h*0.4)
        self.time = 0
        self.range = 1
        self.dx = 1
        self.alpha = 255
        self.i = -1
    
    def update(self, dt):
       
        if self.alpha <= 100:
            self.i = 1
            
        elif self.alpha >= 255:
            self.i = -1

        self.alpha += self.i    
        
        #print(self.alpha)
        color =  (250, 250, 250, self.alpha)
        self.main_label.color = color
    
    def draw(self):
        self.batch.draw()

class LevelInit(object):
    def __init__(self, width, height, name):
        self.win_w = width
        self.win_h = height
        self.name = name
        self.BCKND_COLOR = [0, 0, 0, 1]
        self.END = False
        self.batch = pyglet.graphics.Batch()
        self._init()
    
    def _init(self):
        self.label = pyglet.text.Label('WELCOME TO', anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=52, color=RED, batch=self.batch, x=self.win_w//2, y=self.win_h*0.6)
        self.main_label = pyglet.text.Label(self.name, anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=22, color=WHITE, batch=self.batch, x=self.win_w//2, y=self.win_h*0.4)
        self.time = 0
        self.range = 3
        
    def update(self, dt):
        self.time += dt
        if self.time >= self.range:
            self.END = True
    
    def draw(self):
        self.batch.draw()
        
class Game(object):
    def __init__(self, width, height, name):
        self.win_w = width
        self.win_h = height
        self.name = name
        self.BCKND_COLOR = rgb_to_pyglet(SKY)
        self.END = False
        self.physics = World()
        
        self.batch = pyglet.graphics.Batch()
        self.camera_x = self.win_w / 2
        self.camera_y = self.win_h / 2
        self._init()
    
    def _init(self):
        self.map = Map('resources/maps/lvl2.txt', self.physics)
        
        self.map.create_actors(self.batch)
        self.player = Player(self.physics, rgb_to_pyglet(PLAYER), 100, 100, 16, 25)
        self.game = Rules(self.player, self.map.width, self.map.height)
        self.right_move = False
        self.left_move = False
        
        
    def setup2d(self):
        glColor3ub(255,255,255)
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self.win_w, self.win_h) 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.win_w, 0, self.win_h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def update(self, dt):
        
        self.player.move_down(dt)
        self.player.move_right(dt)
        self.player.move_left(dt)
        self.player.move_up(dt)
        
        self.camera_x = self.player.x - (self.win_w / 2)
        self.camera_y = self.player.y - (self.win_h / 2)
        
        #stage borders
        self.game.StageBorder(self.player.x, self.player.y)
        
        #self.platform.Move()
        
        
        
                   
        if self.player.jumping == True:
            #self.label.text = 'jump'
            height = self.player.y - self.player.jumppoint
            sp = height/JUMP_HEIGHT
            sp = np.cos(sp*np.pi/2)
            if sp > 0.25:
                self.player.up_vel += sp * 10
            else:
                self.player.jumppoint = self.player.y
                self.player.jumping = False
        
        #check if player touches any walls, flours etc
        #+gravitation and jumping bool
        self.physics.TouchCheck(self.player)
        if len(self.physics.collide_d) > 0:
            #self.player.jumping = False
            friction = FRICTION
            for block in self.physics.collide_d:
                if block.enemy:
                    #self.game.player_live = False
                    self.game.DeathBlockCollision()
                if type(block) == MovingPlatform:
                    self.player.x += block.dx
                    
        else:
            friction = FLYING_MOVESPEED
            if self.player.down_vel < GRAVITY:
                self.player.down_vel += 0.1 * GRAVITY
            else:
                self.player.down_vel = GRAVITY
           
        if len(self.physics.collide_r) > 0:
            for block in self.physics.collide_r:
                if block.enemy:
                    #self.game.player_live = False
                    self.game.DeathBlockCollision()
                    
        
        if len(self.physics.collide_u) > 0:
            for block in self.physics.collide_u:
                if block.enemy:
                    #self.game.player_live = False
                    self.game.DeathBlockCollision()
                    
        
        if len(self.physics.collide_l) > 0:
            for block in self.physics.collide_l:
                if block.enemy:
                    #self.game.player_live = False
                    self.game.DeathBlockCollision()
                    
        
        
          #game events check
        if not self.game.player_live:
            self.Restart()
            
        if self.physics.warp_collide:
            self.game.victory = True
            
        
        
        if self.player.up_vel > 0:
            self.player.up_vel -= 0.1 * self.player.max_speed
        else:
            self.player.up_vel = 0
            
        if self.player.down_vel > 0:
            self.player.down_vel -= 0.1 * self.player.max_speed 
        else:
            self.player.down_vel = 0
        
        #velocity of right direction
        if self.right_move:
            if self.player.right_vel < self.player.max_speed:
                self.player.right_vel += 0.1 * self.player.max_speed * friction
            else:
                self.player.right_vel = self.player.max_speed * friction
        else:
            if self.player.right_vel > 0:
                self.player.right_vel -= 0.1 * self.player.max_speed * friction * INERTION
            else:
                self.player.right_vel = 0
        

        #velocity of left direction
        if self.left_move:
            if self.player.left_vel < self.player.max_speed:
                self.player.left_vel += 0.1 * self.player.max_speed * friction
            else:
                self.player.left_vel = self.player.max_speed * friction
        else:
            if self.player.left_vel > 0:
                self.player.left_vel -= 0.1 * self.player.max_speed * friction * INERTION
            else:
                self.player.left_vel = 0
                
        
    
    def draw_all(self):
        glTranslatef(-self.camera_x, -self.camera_y - self.player.height, 0)
        self.batch.draw()
        self.player.draw()
        self.setup2d()  
    
    def draw(self):
        self.draw_all()
        
    def jump_move(self):
        if len(self.physics.collide_d) > 0:
                #self.player.up_vel = JUMP_HEIGHT
                self.player.jumppoint = self.player.y
                self.player.jumping = True

