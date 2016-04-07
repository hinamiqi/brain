#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#import PIL
import PIL.Image

im = PIL.Image.open("map3.bmp")
# rgb = im.getpixel((1,1))
# print(rgb)

def LoadLevel():
    level = []
    for i in range(16):
        level.append([])
        for j in range(16):
            if im.getpixel((j,i)) == (0, 0, 0):
                level[i].append(1) #static block
            elif im.getpixel((j,i)) == (255, 0, 0):
                level[i].append(2) #death block
            elif im.getpixel((j,i)) == (0, 255, 0):
                level[i].append(3) #way out
            else:
                level[i].append(0)
    return level

