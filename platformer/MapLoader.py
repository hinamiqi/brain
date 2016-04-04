#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#import PIL
import PIL.Image

im = PIL.Image.open("map.bmp")
# rgb = im.getpixel((1,1))
# print(rgb)

def LoadLevel():
    level = []
    for i in range(10):
        level.append([])
        for j in range(10):
            if im.getpixel((j,i)) == (0, 0, 0):
                level[i].append(1)
            else:
                level[i].append(0)
    return level

