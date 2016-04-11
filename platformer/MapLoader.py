#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#import PIL
import PIL.Image

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

