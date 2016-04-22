#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json

from Actors import *

def load_data(filename):
    with open(filename, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    objects = {}
    for obj in data['objects']:
        objects[(obj['cord'][0],obj['cord'][1])] = obj

    name = data['name']
    width = data['width']
    height = data['height']
    if 'start_pos' in data:
        start_pos = data['start_pos']
    else:
        start_pos = (100, 100)

    return objects, name, width, height, start_pos

class Map(object):
    '''
    Load all "blocks" in World object.
    map - list 10*10 of 1's and 0's
    physics - object which contains all static blocks (x,y, width,
    height, color)
       
    '''
    
    def __init__(self, path, physics):
        self.objects, self.name, self.width, self.height, self.start_pos = load_data(path)
        self.physics = physics
        self.x_border = [0, self.width * 32]
        self.y_border = [0, self.height * 32]

 
    def create_actors(self, batch):
        for key in self.objects:
            obj = self.objects[key]
            x, y = obj['cord']
            if obj['type'] == 'warp':
                block = Actor(obj['color'], x*32+8, y*32+8, 16, 16, type=obj['type'])
            elif obj['type'] == 'block':
                block = Actor(obj['color'], x*32, y*32, 32, 32, type=obj['type'])
            elif obj['type'] == 'dblock':
                block = Actor(obj['color'], x * 32, y * 32, 32, 16, enemy=True, type=obj['type'])
            else:
                continue
            #block = Actor(obj['color'], x*32, y*32, 32, 32, type=obj['type'])
            self.physics.add_object(block)
            #block.AddToBatch(batch)
            block.create_sprite(batch)