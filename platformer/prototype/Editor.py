#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import pickle
import json

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]
dblockColor = [227, 38, 54]
warpColor = [102, 204, 102]
redColor = [255, 0, 0]

STEP = 32
PATH = 'resources/maps/'


class Map(object):
    
    def __init__(self, objects, name, width, height ):
        self.batch = pyglet.graphics.Batch()
        self.objects = objects
        self.width = width
        self.height = height
        self.name = name
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
        for i in range(self.width):
            self.draw_line([i*self.step, 0, i*self.step, self.win_h])
        for j in range(self.height):
            self.draw_line([0, j*self.step, self.win_w, j*self.step])


class Window(pyglet.window.Window):

    def __init__(self, map):
        super().__init__(512, 512)
        self.map = map
        #background color
        pyglet.gl.glClearColor(*rgb_to_pyglet(backgroundColor))
        
        
        
    def on_draw(self):
        self.clear()
        
        self.map.batch.draw()
        grid.draw()
    
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
                # print('Coords: ', x, y)
                print( grid_snap(STEP, x, y))
                
                x, y = grid_snap(STEP, x, y)
                #create_obj(self.map, x, y, 'tile')
                self.map.add_object({'cord':(x, y), 'type':'block', 'color':blockColor})
                #self.map.load_map()
                #self.map.create_tiles()
                #map.add_to_batch()
                #self.on_draw()
        elif button == pyglet.window.mouse.RIGHT:
            position = grid_snap(STEP, x, y)
            self.map.objects.pop(position)
            self.map.tiles[position].delete()
            #self.map.load_map()

            
    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.S:
            filename = PATH + input('Save as.. ')
            self.map.save_map(filename)
            
        elif key == pyglet.window.key.O:
            filename = PATH + input('Open.. ')
            self.map = Map(*load_map(filename))
            
        elif key == pyglet.window.key.I:
            print(self.map.objects)
           

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