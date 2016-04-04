#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
from Actors import *
from Physics import World
from MapLoader import *


#Colors const.

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]

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
    
    def CreateActors(self):
        i = 10
        j = -1
        for row in self.map:
            i -= 1
            j = -1
            for col in row:
                j += 1
                #blocks
                if col == 1:
                    print(i, j)
                    block = Actor(rgb_to_pyglet(blockColor), j*50, i*50, 50, 50)
                    self.blocks.append(block)
                    self.physics.AddObject(block)
                    
  
       
       
class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(500, 500)
     
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
        
        '''player object.
        Params:
        World - all object to interact
        Color
        x
        y
        width
        height
        '''
        self.player = Player(self.physics, rgb_to_pyglet(playerColor), 100, 300, 15, 30)
        
        #create blocks from level file
        self.map.CreateActors()
        
        #label for some info
        self.label = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=10, y=440,
                                           anchor_x='left', anchor_y='bottom')
        
        #call update() every 1/60 s
        pyglet.clock.schedule_interval(self.update, 1/60)

  
    def draw_all(self):
        #draw all the things 
        self.clear()
        self.player.draw()
        self.label.draw()
        for block in self.map.blocks:
            block.draw()

    def update(self, dt):
        
        #update position of player 
        self.player.move_up(dt)
        self.player.move_down(dt)
        self.player.move_right(dt)
        self.player.move_left(dt)
        
        #check if player touches any walls, flours etc
        #+gravitation and jumping bool
        if self.physics.TouchCheck(self.player):
            self.player.jumping = False
            friction = 1
            self.label.text = 'Ground'
        else:
            friction = 0.4
            if self.player.down_vel < 10:
                self.player.down_vel += 0.1 * self.physics.grav_const
            else:
                self.player.down_vel = 10
            self.label.text = 'Air'
            
        #velocity of up direction
        if self.key_holder['Up']:
            if self.player.up_vel < self.player.max_speed:
            
                self.player.up_vel += 0.1 * 20
            else:
                self.player.up_vel = 20

        else:
            if self.player.up_vel > 0:
                self.player.up_vel -= 0.1 * self.player.max_speed
            else:
                self.player.up_vel = 0
    

        #velocity of down direction
        if self.key_holder['Down']:
            if self.player.down_vel < self.player.max_speed:
                self.player.down_vel += 0.1 * self.player.max_speed
            else:
                self.player.down_vel = self.player.max_speed
        # else:
            # if self.player.down_vel < 10:
                # self.player.down_vel += 0.1 * self.player.max_speed 
            # else:
                # self.player.down_vel = 10
        

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
        
        #and draw everything
        self.draw_all()
        
        
        
        


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
                self.player.up_vel = 20
                self.player.jumping = True
        elif key == pyglet.window.key.R:
            #reset all player vars
            self.player.x = 100
            self.player.y = 300
            self.player.up_vel = 0
            self.player.down_vel = 5
            self.player.left_vel = 0
            self.player.right_vel = 0
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