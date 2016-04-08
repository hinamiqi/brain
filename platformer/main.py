#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import numpy as np

from pyglet.gl import *
from math import copysign, sin, cos, pi

from Rules import *
from Actors import *
from Physics import World
from MapLoader import *
from Menu import *


#Const.

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]
dblockColor = [227, 38, 54]
warpColor = [102, 204, 102]
redColor = [255, 0, 0]

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
#list 10*10: 1- block, 0 - None        
level = LoadLevel()

       
class Map(object):
    '''
    Load all "blocks" in World object.
    map - list 10*10 of 1's and 0's
    physics - object which contains all static blocks (x,y, width,
    height, color)
       
    '''
    
    def __init__(self, map, physics):
        self.map = map
        self.physics = physics
        self.blocks = []
        self.x = 100
        self.y = 300
        
    def CreateActors(self, batch):
        i = 16
        j = -1
        for row in self.map:
            i -= 1
            j = -1
            for col in row:
                j += 1
                #blocks
                if col != 0:
                    if col == 1:
                        #print(i, j)
                        block = Actor(blockColor, j*32, i*32, 32, 32)
                        self.blocks.append(block)
                        self.physics.AddObject(block)
                    elif col == 2:
                        block = Actor(dblockColor, j*32, i*32, 32, 32, enemy=True)
                        self.blocks.append(block)
                        self.physics.AddObject(block)
                    elif col == 3:
                        block = Actor(warpColor, j*32+8, i*32+8, 16, 16, warp=True)
                        self.blocks.append(block)
                        self.physics.AddObject(block)
                    elif col == 4:
                        self.x, self.y = j*32, i*32
                    block.AddToBatch(batch)
                    
  
       
       
class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(512, 512)
     
        #background color
        pyglet.gl.glClearColor(*rgb_to_pyglet(backgroundColor))
        
        #for the keys state
        self.key_holder = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
        
        #object to carry all static blocks
        self.physics = World()
        
        '''
        load map list from image file. Image 10*10 b&w. Black pixel-
        block, white - None
        '''
#         self.map = Map(level, self.physics)
        self.map = None
       
    
        '''
        Menu object
        '''
        self.menu = GameMenu(x = lambda: self.width // 2.5, y = lambda: self.height // 1.5, 
            height = lambda: self.height)
        
        '''player object.
        Params:
        World - all object to interact
        Color
        x
        y
        width
        height
        '''
        
        #create blocks from level file
        self.batch = pyglet.graphics.Batch()
#         self.map.CreateActors(self.batch)
        
        #self.player = Player(self.physics, rgb_to_pyglet(playerColor), 100, 300, 16, 32)
#         self.player = Player(self.physics, rgb_to_pyglet(playerColor), self.map.x, self.map.y, 16, 25)
       
        
        #object for all game events, vars etc
        # self.game = Game(self.player)
        self.game = None
        
        #label for some info
        self.label = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=10, y=460,
                                           anchor_x='left', anchor_y='bottom')
        
        self.label2 = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=30, y=460,
                                           anchor_x='left', anchor_y='bottom')                                   
        self.victory_msg = pyglet.text.Label("Teh WINRAR is YOU!", font_name='Arial', font_size=35, 
                                           x=256, y=256,
                                           anchor_x='center', anchor_y='center')
        
        self.fps_display = pyglet.clock.ClockDisplay()
        
        #camera
        self.camera_x = self._width / 2
        self.camera_y = self._height / 2
       
        self.time = 0
        
        #call update() every 1/60 s
        pyglet.clock.schedule_interval(self.update, 1/60)
        
        

    def setup2d(self):
       
        
        glColor3ub(255,255,255)
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self._width, self._height) 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
  
            
    def draw_all(self):
        self.setup2d()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if self.map:
            self.draw_game()
        else:
            self.menu.draw()
    
    def draw_game(self):
        glTranslatef(-self.camera_x, -self.camera_y - self.player.height, 0)
        #draw all the things 
        if self.game.victory:
            self.clear()
            self.victory_msg.draw()
        else:
            self.clear()
            # for block in self.map.blocks:
                # block.draw()
            self.batch.draw()
            self.player.draw()
        self.setup2d()  
        
        self.label.draw()  
        
        self.label2.draw()
        self.fps_display.draw()
    
    def Invuln(self):
        if self.time > 60:
            self.player.invuln = False
            self.time = 0
            self.player.color = rgb_to_pyglet(playerColor)
        else:
            self.time += 1
            if self.time % 5 == 0:
                self.player.color = [1, 0, 0]
            else:
                self.player.color = rgb_to_pyglet(playerColor)
        
    
    def update(self, dt):
        if not self.map: 
            self.draw_all()
            return
        # self.label.text = 'up: ' + str(round(self.player.up_vel)) + \
                          # ' down: ' + str(round(self.player.down_vel)) + \
                          # ' right: ' + str(round(self.player.right_vel)) + \
                          # ' left: ' + str(round(self.player.left_vel)) 
        
        #self.label.text = str(self.physics.collide)
        
        self.label.text = str(self.game.player_hp)
        
        if self.player.invuln:
            self.Invuln()
            self.label2.text = 'inv'
        else:
            self.label2.text = ''
            #print('yay')
        #update position of player 
        
        self.player.move_down(dt)
        self.player.move_right(dt)
        self.player.move_left(dt)
        self.player.move_up(dt)
        
        self.camera_x = self.player.x - (self._width / 2)
        self.camera_y = self.player.y - (self._height / 2)
        
        #stage borders
        self.game.StageBorder(self.player.x, self.player.y)
        
                   
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
        if self.key_holder['Right']:
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
        if self.key_holder['Left']:
            if self.player.left_vel < self.player.max_speed:
                self.player.left_vel += 0.1 * self.player.max_speed * friction
            else:
                self.player.left_vel = self.player.max_speed * friction
        else:
            if self.player.left_vel > 0:
                self.player.left_vel -= 0.1 * self.player.max_speed * friction * INERTION
            else:
                self.player.left_vel = 0
                
     
        
      
        #self.label.text = str(self.game.victory)
        
        #and draw everything
        self.draw_all()
        
    
    
    def Restart(self):
        #reset all player vars
        self.player.x = self.map.x
        self.player.y = self.map.y
        self.player.up_vel = 0
        self.player.down_vel = 0
        self.player.left_vel = 0
        self.player.right_vel = 0
        self.game.player_live = True
        self.game.player_hp = 3
        self.player.invuln = False
        self.time = 0
        self.game.victory = False

       
        
        

    def on_key_press(self, key, modifiers):
        if not self.map:
            if key == pyglet.window.key.DOWN:
                self.menu.select_next()
            elif key == pyglet.window.key.UP:
                self.menu.select_previous()
            elif key == pyglet.window.key.RETURN:
                self.map = Map(LoadLevel(self.menu.levels[self.menu.selected]), self.physics)
                self.map.CreateActors(self.batch)
                self.player = Player(self.physics, rgb_to_pyglet(playerColor), self.map.x, self.map.y, 16, 25)
                self.game = Game(self.player)
            elif key == pyglet.window.key.ESCAPE:
                pyglet.app.exit()
            return
    
        if key == pyglet.window.key.UP:
            self.key_holder['Up'] = True
        elif key == pyglet.window.key.DOWN:
            self.key_holder['Down'] = True
        elif key == pyglet.window.key.RIGHT:
            self.key_holder['Right'] = True
        elif key == pyglet.window.key.LEFT:
            self.key_holder['Left'] = True
        elif key == pyglet.window.key.SPACE:
            if len(self.physics.collide_d) > 0:
                #self.player.up_vel = JUMP_HEIGHT
                self.player.jumppoint = self.player.y
                self.player.jumping = True
        elif key == pyglet.window.key.R:
            self.Restart()
        #camera
        elif key == pyglet.window.key.W:
            self.camera_y -= 50
        elif key == pyglet.window.key.S:
            self.camera_y += 50
        elif key == pyglet.window.key.D:
            self.camera_x -= 50
        elif key == pyglet.window.key.A:
            self.camera_x += 50
            
        elif key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
         

    def on_key_release(self, key, modifiers):
        if key == pyglet.window.key.UP:
            self.key_holder['Up'] = False
        elif key == pyglet.window.key.DOWN:
            self.key_holder['Down'] = False
        elif key == pyglet.window.key.RIGHT:
            self.key_holder['Right'] = False
        elif key == pyglet.window.key.LEFT:
            self.key_holder['Left'] = False
        
        

#normalize 0-255 to 0-1
def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result


if __name__ == '__main__':
    window = Window()
    pyglet.app.run()