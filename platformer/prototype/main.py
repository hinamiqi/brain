#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

from pyglet.gl import *
from pyglet.window import key

from Scenes import *

backgroundColor = [176, 224, 230, 255]

class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(512, 512)
        self.state = StateHandler()
        self.scene = self.state.scene
        pyglet.gl.glClearColor(*self.scene.BCKND_COLOR)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.label = pyglet.text.Label('', anchor_x="left", anchor_y="top", 
                font_name='Arial', font_size=12, x=0, y=512)
        pyglet.clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        self.state.keys = keys
        self.scene = self.state.scene
        self.scene.update(dt)
        self.label.text = self.state.msg
        # if keys[key.ENTER]:
            # self.state.scene = LevelInit(self.state, 512, 512, 'SCARY CEMETERY')
        # if keys[key.RIGHT]:
            # self.scene.right_move = True
        # elif keys[key.LEFT]:
            # self.scene.left_move = True
        # if keys[key.SPACE]:
            # self.scene.jump_move()
        if keys[key.ESCAPE]:
            pyglet.app.exit()
            
        
    def on_key_press(self, key, modifiers):
        self.scene.key_pressed(key)
        
    def on_draw(self):
    
        self.clear()
        pyglet.gl.glClearColor(*self.scene.BCKND_COLOR)
        self.scene.draw()
        self.label.draw()
        self.fps_display.draw()
    
    

#normalize 0-255 to 0-1
def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result


if __name__ == '__main__':
    window = Window()
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    pyglet.app.run()