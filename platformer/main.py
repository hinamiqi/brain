#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
from Actors import *
from Physics import World
from MapLoader import *

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]

# level = [
        # [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        # [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        # [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        # [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        # [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        # [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        # [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        # [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       # ]
       
level = LoadLevel()
       
class Map(object):
    
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
        # pyglet.gl.glColor3f(*rgb_to_pyglet(backgroundColor))
        pyglet.gl.glClearColor(*rgb_to_pyglet(backgroundColor))

        self.key_holder = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
        self.physics = World()
        self.map = Map(level, self.physics)
        self.player = Player(self.physics, rgb_to_pyglet(playerColor), 100, 300, 15, 50)
        self.map.CreateActors()
        #print(self.map.blocks)
        # self.block = Actor(rgb_to_pyglet(blockColor), 100, 200, 100, 50)
        # self.block1 = Actor(rgb_to_pyglet(blockColor), 0, 50, 300, 50)
        # self.block2 = Actor(rgb_to_pyglet(blockColor), 300, 50, 100, 100)
        
        # self.physics.AddObject(self.block)
        # self.physics.AddObject(self.block1)
        # self.physics.AddObject(self.block2)
        self.label = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=10, y=440,
                                           anchor_x='left', anchor_y='bottom')
        pyglet.clock.schedule_interval(self.update, 1/60)

  
    def draw_all(self):
        self.clear()
        self.player.draw()
        # self.block.draw()
        # self.block1.draw()
        # self.block2.draw()
        self.label.draw()
        for block in self.map.blocks:
            
            block.draw()

    def update(self, dt):

        #self.player.CollisionCheck(self.block)
        
        # if self.physics.CollisionCheck(self.player, self.block):
            # self.label.text = 'Yay!'
        # else:
            # self.label.text = ''
        # if self.physics.CollisionCheck(self.player):
            # self.label.text = 'Collision!'
        # else:
            # self.label.text = ''
            # self.player.Moving()
        #self.player.down_vel += self.physics.Gravitation(self.player.down_vel)
        self.player.move_up(dt)
        self.player.move_down(dt)
        self.player.move_right(dt)
        self.player.move_left(dt)
        
        
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
            
        #move up:
        # if self.key_holder['Up']:
            # if self.player.up_vel < self.player.max_speed:
            
                # self.player.up_vel += 0.1 * self.player.max_speed
            # else:
                # self.player.up_vel = self.player.max_speed

        # else:
        if self.player.up_vel > 0:
            self.player.up_vel -= 0.1 * self.player.max_speed
        else:
            self.player.up_vel = 0
    

        #move down:
        # if self.key_holder['Down']:
            # if self.player.down_vel < self.player.max_speed:
                # self.player.down_vel += 0.1 * self.player.max_speed
            # else:
                # self.player.down_vel = self.player.max_speed
        # else:
            # if self.player.down_vel < 10:
                # self.player.down_vel += 0.1 * self.player.max_speed 
            # else:
                # self.player.down_vel = 10
        

        #move right:
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
        

        #move left:
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


def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result


if __name__ == '__main__':
    window = Window()
    pyglet.app.run()