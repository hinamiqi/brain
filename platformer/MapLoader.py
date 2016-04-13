#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#import PIL
import PIL.Image
import json


# rgb = im.getpixel((1,1))
# print(rgb)

def LoadLevel(path="map1.bmp"):
    im = PIL.Image.open(path)
    level = []
    width, height = im.size
    for i in range(height):
        level.append([])
        for j in range(width):
            if im.getpixel((j,i)) == (0, 0, 0):
                level[i].append(1) #static block
            elif im.getpixel((j,i)) == (255, 0, 0):
                level[i].append(2) #death block
            elif im.getpixel((j,i)) == (0, 255, 0):
                level[i].append(3) #way out
            elif im.getpixel((j,i)) == (0, 0, 255):
                level[i].append(4) #start
            else:
                level[i].append(0)

    return level, width, height

def LoadLevel2(path="lvl1.txt"):
    level = []
    objects, name, width, height = load_map(path)
    # for i in range(height):
        # level.append([])
        # for j in range(width):
            # level[i].append(0)
   
    # for key in objects:
        # if objects[key]['type'] == 'block':
            # level[key[1]][key[0]-height] = 1
    for i in range(height):
        level.append([])
        for j in range(width):
            if (j,i) in objects:
                level[i].append(1)
            else:
                level[i].append(0)
    print(level)
    return level, width, height
    
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
