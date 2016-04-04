#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#import PIL
import PIL.Image

im = PIL.Image.open("map.bmp")
rgb = im.getpixel((1,1))
print(rgb)