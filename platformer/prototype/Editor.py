#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import json

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import HorizontalContainer
from pyglet_gui.theme import Theme
from pyglet_gui.constants import *

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
startColor = [10, 10, 250]
pointColor = [250, 250, 10]
blockColor = [184, 134, 11]
dblockColor = [227, 38, 54]
warpColor = [102, 204, 102]
redColor = [255, 0, 0]

STEP = 32
PATH = 'resources/maps/'

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "button": {
                   "down": {
                       "image": {
                           "source": "button-down.png",
                           "frame": [6, 6, 3, 3],
                           "padding": [12, 12, 4, 2]
                       },
                       "text_color": [0, 0, 0, 255]
                   },
                   "up": {
                       "image": {
                           "source": "button.png",
                           "frame": [6, 6, 3, 3],
                           "padding": [12, 12, 4, 2]
                       }
                   }
               },
               "checkbox": {
                   "checked": {
                       "image": {
                           "source": "checkbox-checked.png"
                       }
                   },
                   "unchecked": {
                       "image": {
                           "source": "checkbox.png"
                       }
                   }
               }
              }, resources_path='theme/')

class Map(object):
    
    def __init__(self, objects, name, width, height ):
        self.batch = pyglet.graphics.Batch()
        self.objects = objects
        self.width = width
        self.height = height
        self.name = name
        self.start_pos = None
        self.tiles = {}
        for key in self.objects:
            self.add_tile(self.objects[key])
    
    def _verts(self, obj):
        x, y = obj['cord']
        verts = [x*STEP, y*STEP,
                 x*STEP + STEP, y*STEP,
                 x*STEP + STEP, y*STEP + STEP,
                 x*STEP, y*STEP + STEP]
        return verts
    
    def add_object(self, obj):
        x, y = obj['cord']
        position = (x, y)
        if not position in self.objects:
            self.objects[position] = obj
            self.add_tile(obj)
        
        
    def add_tile(self, obj):
        x, y = obj['cord']
        position = (x, y)
        color = []
        for i in range(4):
            color.extend(obj['color'])
        
        self.tiles[position] = self.batch.add(4, \
                                              pyglet.gl.GL_QUADS, \
                                              None, \
                                              ('v2f/static', self._verts(obj)), \
                                              ('c3B', color))
  
    def draw_start(self):
        pyglet.gl.glColor3f(*rgb_to_pyglet(startColor))
        x, y = self.start_pos
        print(x, y)
        pyglet.graphics.draw(4, \
                             pyglet.gl.GL_QUADS, \
                             None, \
                             ('v2f/static', [x, y, x+STEP, y, x, y+STEP, x+STEP, y+STEP ]))
    
    def save_map(self, filename):
        objects = []
        for key in self.objects:
            objects.append(self.objects[key])
        data = {
                    'objects':objects,
                    'name':self.name,
                    'width':self.width,
                    'height':self.height
        
                }
        print('Saved as ', filename)
        with open(filename, 'w', encoding='utf-8') as data_file:
            json.dump(data, data_file)
    
def load_map(filename):
    with open(filename, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    objects = {}
    for obj in data['objects']:
        objects[(obj['cord'][0],obj['cord'][1])] = obj

    name = data['name']
    width = data['width']
    height = data['height']

    return objects, name, width, height


class Grid(object):
    
    def __init__(self, step, window):
        self.step = step
        #self.window = window
        self.win_w = window._width 
        self.win_h = window._height 
        self.width = self.win_w // self.step
        self.height = self.win_h // self.step
    
    def draw_line(self, verts):
        pyglet.gl.glColor3f(1, 1, 1)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, \
                        ('v2f', verts))
    def draw(self):
        for i in range(1, self.width):
            self.draw_line([i*self.step, self.step, i*self.step, self.win_h-self.step])
        for j in range(1, self.height):
            self.draw_line([self.step, j*self.step, self.win_w-self.step, j*self.step])


class Window(pyglet.window.Window):

    def __init__(self, map):
        super().__init__(576, 576)
        self.map = map
        #background color
        pyglet.gl.glClearColor(*rgb_to_pyglet(backgroundColor))
        self._init_gui()
        
        
    def _init_gui(self):
        self.gui_batch = pyglet.graphics.Batch()
        self.button1 = GroupButton(group_id='1', label="Block")
        self.button2 = GroupButton(group_id='1', label="Death block")
        self.button3 = GroupButton(group_id='1', label="Start")
        self.button4 = GroupButton(group_id='1', label="Warp")
        self.button5 = GroupButton(group_id='1', label="Point")
        self.button6 = OneTimeButton(label="Save")
        self.button7 = OneTimeButton(label="Open")
        self.button8 = OneTimeButton(label="Exit")
        Manager(HorizontalContainer([
                               self.button1,
                               self.button2,
                               self.button3,
                               self.button4,
                               self.button5
                               ]),
            window=self,
            is_movable=False,
            anchor=ANCHOR_BOTTOM_RIGHT,
            batch=self.gui_batch,
            theme=theme)
        
        Manager(HorizontalContainer([
                               self.button6,
                               self.button7,
                               self.button8
                               ]),
            window=self,
            is_movable=False,
            anchor=ANCHOR_TOP_LEFT,
            batch=self.gui_batch,
            theme=theme)
            
    def on_draw(self):
        self.clear()
        self.map.batch.draw()
        if self.map.start_pos:
            #print(self.map.start_pos)
            self.draw_start()
        grid.draw()
        self.gui_batch.draw()
        
    def draw_start(self):
        x, y = self.map.start_pos
        pyglet.gl.glColor3f(*rgb_to_pyglet(startColor))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
                        ('v2f', (x*STEP, y*STEP,
                        x*STEP + STEP, y*STEP,
                        x*STEP + STEP, y*STEP + STEP,
                        x*STEP, y*STEP + STEP)))
    
    def callback(self, is_pressed):
        print('yay')
    
    def on_mouse_press(self, x, y, button, modifiers):
        if STEP < x < self._width - STEP and STEP < y < self._height - STEP:
            if button == pyglet.window.mouse.LEFT:
                    print( grid_snap(STEP, x, y))
                    position = grid_snap(STEP, x, y)
                    if self.button1.is_pressed:
                        type = 'block'
                        color = blockColor
                    elif self.button2.is_pressed:
                        type = 'dblock'
                        color = dblockColor
                    elif self.button3.is_pressed:
                        self.map.start_pos = position
                        
                    elif self.button4.is_pressed:
                        type = 'warp'
                        color = warpColor
                    elif self.button5.is_pressed:
                        type = 'point'
                        color = pointColor
                    
                    try:
                        if self.map.objects[position]:
                            self.map.objects.pop(position)
                            self.map.tiles[position].delete()
                    except:
                        pass
                    
                    try:
                        self.map.add_object({'cord':position, 'type':type, 'color':color})
                    except:
                        pass
            elif button == pyglet.window.mouse.RIGHT:
                position = grid_snap(STEP, x, y)
                self.map.objects.pop(position)
                self.map.tiles[position].delete()


            
    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.S:
            filename = PATH + input('Save as.. ')
            self.map.save_map(filename)
            
        elif key == pyglet.window.key.O:
            filename = PATH + input('Open.. ')
            self.map = Map(*load_map(filename))
            
        elif key == pyglet.window.key.I:
            print(self.map.objects)
        
        elif key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

def create_obj(map, x, y, type):
    obj = {'cord':(x, y), 'type':type, 'color':blockColor}
    map.objects.append(obj)

def remove_obj(map, x, y, type):
    obj = {'cord':(x, y), 'type':type, 'color':blockColor}
    map.objects.remove(obj)
    
def grid_snap(step, x, y):
    gx = x // step 
    gy = y // step
    return gx, gy

        
#normalize 0-255 to 0-1
def rgb_to_pyglet(list):
    result = []
    for i in list:
        result.append(i/255)
    return result
        

        

        
if __name__ == '__main__':
    map = Map(objects = {}, name = 'Untitled1', width = 16, height = 16)
    window = Window(map)
    grid = Grid(STEP, window)
    
    
    
    pyglet.app.run()