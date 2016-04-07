#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
from Rules import *
from Actors import *
from Physics import World
from MapLoader import *


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
JUMP_HEIGHT = 15
#0-1
FRICTION = 0.8

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
    
    def CreateActors(self, batch):
        i = 16
        j = -1
        for row in self.map:
            i -= 1
            j = -1
            for col in row:
                j += 1
                #blocks
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
        self.map = Map(level, self.physics)
        
        #object for all game events, vars etc
        self.game = Game()
        
        '''player object.
        Params:
        World - all object to interact
        Color
        x
        y
        width
        height
        '''
        self.player = Player(self.physics, rgb_to_pyglet(playerColor), 100, 300, 16, 32)
        
        self.batch = pyglet.graphics.Batch()
        
        #create blocks from level file
        self.map.CreateActors(self.batch)
        
        #label for some info
        self.label = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=10, y=460,
                                           anchor_x='left', anchor_y='bottom')
                                           
        self.victory_msg = pyglet.text.Label("Teh WINRAR is YOU!", font_name='Arial', font_size=35, 
                                           x=256, y=256,
                                           anchor_x='center', anchor_y='center')
        
        self.fps_display = pyglet.clock.ClockDisplay()
        
        #call update() every 1/60 s
        pyglet.clock.schedule_interval(self.update, 1/60)
        
        

  
  
            
    def draw_all(self):
        #draw all the things 
        
        
        if self.game.victory:
            self.clear()
            self.victory_msg.draw()
            self.label.draw()
        else:
            
            self.clear()
            # for block in self.map.blocks:
                # block.draw()
            self.batch.draw()
            self.player.draw()
            self.label.draw()
            
        self.fps_display.draw()

    def update(self, dt):
        # self.label.text = 'up: ' + str(round(self.player.up_vel)) + \
                          # ' down: ' + str(round(self.player.down_vel)) + \
                          # ' right: ' + str(round(self.player.right_vel)) + \
                          # ' left: ' + str(round(self.player.left_vel)) 
        
        #self.label.text = str(self.physics.collide)
        #update position of player 
        
        self.player.move_down(dt)
        self.player.move_right(dt)
        self.player.move_left(dt)
        self.player.move_up(dt)
        
        #check if player touches any walls, flours etc
        #+gravitation and jumping bool
        self.physics.TouchCheck(self.player)
        if len(self.physics.collide_d) > 0:
            self.player.jumping = False
            friction = FRICTION
            for block in self.physics.collide_d:
                if block.enemy:
                    self.game.player_live = False
        else:
            friction = FLYING_MOVESPEED
            if self.player.down_vel < GRAVITY:
                self.player.down_vel += 0.1 * GRAVITY
            else:
                self.player.down_vel = GRAVITY
           
        if len(self.physics.collide_r) > 0:
            for block in self.physics.collide_r:
                if block.enemy:
                    self.game.player_live = False
        
        if len(self.physics.collide_u) > 0:
            for block in self.physics.collide_u:
                if block.enemy:
                    self.game.player_live = False
        
        if len(self.physics.collide_l) > 0:
            for block in self.physics.collide_l:
                if block.enemy:
                    self.game.player_live = False
        
        
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
        
        #velocity of up direction
        # if self.key_holder['Up']:
            # if self.player.up_vel < self.player.max_speed:
            
                # self.player.up_vel += 0.1 * self.player.max_speed
            # else:
                # self.player.up_vel = self.player.max_speed

        # else:
            # if self.player.up_vel > 0:
                # self.player.up_vel -= 0.1 * self.player.max_speed
            # else:
                # self.player.up_vel = 0
        
        
    

        #velocity of down direction
        # if self.key_holder['Down']:
            # if self.player.down_vel < self.player.max_speed:
                # self.player.down_vel += 0.1 * self.player.max_speed
            # else:
                # self.player.down_vel = self.player.max_speed
        # else:
            # if self.player.down_vel > 0:
                # self.player.down_vel -= 0.1 * self.player.max_speed 
            # else:
                # self.player.down_vel = 0
        

        #velocity of right direction
        if self.key_holder['Right']:
            if self.player.right_vel < self.player.max_speed:
                self.player.right_vel += 0.1 * self.player.max_speed * friction
            else:
                self.player.right_vel = self.player.max_speed * friction
        else:
            if self.player.right_vel > 0:
                self.player.right_vel -= 0.1 * self.player.max_speed * friction
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
                self.player.left_vel -= 0.1 * self.player.max_speed * friction
            else:
                self.player.left_vel = 0
        
      
        #self.label.text = str(self.game.victory)
        
        #and draw everything
        self.draw_all()
        
        
    def Restart(self):
        #reset all player vars
        self.player.x = 100
        self.player.y = 300
        self.player.up_vel = 0
        self.player.down_vel = 5
        self.player.left_vel = 0
        self.player.right_vel = 0
        self.game.player_live = True
        self.game.victory = False

       
        
        

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.UP:
            self.key_holder['Up'] = True
        elif key == pyglet.window.key.DOWN:
            self.key_holder['Down'] = True
        elif key == pyglet.window.key.RIGHT:
            self.key_holder['Right'] = True
        elif key == pyglet.window.key.LEFT:
            self.key_holder['Left'] = True
        elif key == pyglet.window.key.SPACE:
            if not self.player.jumping:
                self.player.up_vel = JUMP_HEIGHT
                self.player.jumping = True
        elif key == pyglet.window.key.R:
            self.Restart()
            
            
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