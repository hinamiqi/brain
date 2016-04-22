#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import os
import numpy as np

from pyglet.gl import *
from pyglet.window import key

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
ANIMATION_DELAY = 0.2
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

class StateHandler(object):

    def __init__(self):
        self.scene = TitleScreen(self, 512, 512)
        self.keys = {}
        self.msg = ''
        
class TitleScreen(object):
    
    def __init__(self, state, width, height):
        self.win_w = width
        self.win_h = height
        self.state = state
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
        color =  (250, 250, 250, self.alpha)
        self.main_label.color = color
        if self.state.keys[key.ENTER]:
            self.state.scene = LevelInit(self.state, 512, 512, 'SCARY CEMETERY')
    
    def key_pressed(self, key):
        pass
        
    def draw(self):
        self.batch.draw()

class LevelInit(object):
    def __init__(self, state, width, height, name):
        self.win_w = width
        self.win_h = height
        self.name = name
        self.state = state
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
            self.state.scene = Game(self.state, 512, 512, 'SCARY CEMETERY')
    
    def key_pressed(self, key):
        pass
    
    def draw(self):
        self.batch.draw()
        
class Game(object):

    def __init__(self, state, width, height, name):
        self.win_w = width
        self.win_h = height
        self.name = name
        self.state = state
        self.key_time = 0
        self.count = False
        self.BCKND_COLOR = rgb_to_pyglet(SKY)
        self.END = False
        self.physics = World()
        self.friction = 1
        self.batch = pyglet.graphics.Batch()
        self.camera_x = self.win_w // 2
        self.camera_y = self.win_h // 2
        self._init()
    
    def _init(self):
        self.map = Map('resources/maps/lvl3.txt', self.physics)
        self.map.create_actors(self.batch)
        self.player = Player(self.physics, rgb_to_pyglet(PLAYER), 100, 100, 16, 25)
        self.hud = HUD(self.player, 512, 512)
        #self.game = Rules(self.player, self.map.width, self.map.height)

        
    def setup2d(self):
        # glColor3ub(255,255,255)
        # glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self.win_w, self.win_h) 
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        #glOrtho(0, self.win_w, 0, self.win_h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    
    def update(self, dt):
        
        self.player.update(dt)
        self.move_camera()
        self.hud.update(dt)
        if self.state.keys[key.RIGHT]:
            self.player.moving = 'right'
            self.player.direction = 'right'
        elif self.state.keys[key.LEFT]:
            self.player.moving = 'left'
            self.player.direction = 'left'
        else:
            self.player.moving = None

        self.state.msg = str(self.player.direction)
        if self.count:
            self.key_time += dt
            if self.key_time > ANIMATION_DELAY:
                self.count = False
                self.key_time = 0

        if self.player.y < self.map.y_border[0]:
            self.player.status = 'dead'

        if self.player.status == 'dead':
            self.state.scene = GameOver(self.state, 512, 512)
                
                
      
    def move_camera(self):
        self.camera_x = ((self.player.x - (self.win_w // 2)))
        self.camera_y = ((self.player.y - (self.win_h // 2)))
    
    def key_pressed(self, key):
        if key == pyglet.window.key.SPACE:
            # if not self.count:
            #     self.count = True
            #     #self.player.move_jump()
            #     self.player.move_roll()
            # else:
            #
            #     self.player.move_jump()
            self.player.move_roll()
        elif key == pyglet.window.key.UP:
            self.player.move_jump()
           
    def draw_all(self):
        glTranslatef(-self.camera_x, -self.camera_y-150, 0)
        self.batch.draw()
        self.player.draw()
        self.setup2d()
        self.hud.draw()
    
    def draw(self):
        self.draw_all()

class HUD(object):

    def __init__(self, player, width, height):
        self.win_w = width
        self.win_h = height
        self.player = player
        self.hud_batch = pyglet.graphics.Batch()
        self._init()

    def _init(self):
        self.status_label = pyglet.text.Label('', anchor_x="right", anchor_y="top",
                                              font_name='Algerian', font_size=12, color=WHITE, batch=self.hud_batch,
                                              x=self.win_w, y=self.win_h)

        self.msg_label = pyglet.text.Label('', anchor_x="center", anchor_y="bottom",
                                           font_name='Algerian', font_size=12, color=WHITE, batch=self.hud_batch,
                                           x=self.win_w//2, y=10)

        color = []
        for i in range(3):
            color.extend(PLAYER)
        self.hp_bar = self.hud_batch.add(4, pyglet.gl.GL_QUADS, None, \
                                         ('v2f', self._hp_verts()))

    def _hp_verts(self):
        verts = [
                    10,                10, \
                    20,                10, \
                    20,                3*self.player.hp, \
                    10,                3*self.player.hp
        ]

        return verts

    def update(self, dt):
        self.status_label.text = str(self.player.hp)
        self.hp_bar.delete()
        self.hp_bar = self.hud_batch.add(4, pyglet.gl.GL_QUADS, None, \
                                         ('v2f', self._hp_verts()))
        #self.msg_label.text = self.

    def draw(self):
        self.hud_batch.draw()

class GameOver(object):

    def __init__(self, state, width, height):
        self.win_w = width
        self.win_h = height
        self.state = state
        self.BCKND_COLOR = [0, 0, 0, 1]
        self.msg = 'Your friends, family, neighbors and even dog now are dead. And raped.'
        self.batch = pyglet.graphics.Batch()
        self._init()  
            
    def _init(self):
        self.big_label = pyglet.text.Label('GAME OVER', anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=52, color=RED, batch=self.batch, x=self.win_w//2, y=self.win_h*0.6)
        self.small_label = pyglet.text.Label(self.msg, anchor_x="center", anchor_y="center", 
                font_name='Algerian', font_size=22, color=WHITE, batch=self.batch, multiline=True, align="center", x=self.win_w//2, y=self.win_h*0.4, width=0.7*self.win_w)
        self.time = 0
        self.range = 3
        
    def update(self, dt):
        self.time += dt
        if self.time >= 8:
            self.state.scene = TitleScreen(self.state, 512, 512)
    
    def key_pressed(self, key):
        pass
    
    def draw(self):
        self.batch.draw()
        
    
