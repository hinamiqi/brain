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

    return objects, name, width, height

class Map(object):
    '''
    Load all "blocks" in World object.
    map - list 10*10 of 1's and 0's
    physics - object which contains all static blocks (x,y, width,
    height, color)
       
    '''
    
    def __init__(self, path, physics):
        self.objects, self.name, self.width, self.height = load_data(path)
        self.physics = physics
 
    def create_actors(self, batch):
        for key in self.objects:
            obj = self.objects[key]
            #print(obj)
            if obj['type'] == 'block':
                x, y = obj['cord']
                block = Actor(obj['color'], x*32, y*32, 32, 32)
                self.physics.AddObject(block)
                block.AddToBatch(batch)
   