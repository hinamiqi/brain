# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 19:25:50 2016

@author: Modza
"""

from main import Actor
from main import App
from main import rgb_to_pyglet

backgroundColor = [176, 224, 230]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]

screen = App(rgb_to_pyglet(backgroundColor))
player = Actor(rgb_to_pyglet(playerColor), 50, 50, 10, 30)
block = Actor(rgb_to_pyglet(blockColor), 200, 200, 100, 100)
player.draw()
screen.mainLoop()

