#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme

#sys.path.insert(0, os.path.abspath('../'))

import pyglet

window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    window.clear()
    batch.draw()

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
              
Manager(VerticalContainer([Button(label="Persistent button"),
                           OneTimeButton(label="One time button"),
                           Checkbox(label="Checkbox"),
                           GroupButton(group_id='1', label="Group 1:Button 1"),
                           GroupButton(group_id='1', label="Group 1:Button 2"),
                           GroupButton(group_id='2', label="Group 2:Button 1"),
                           GroupButton(group_id='2', label="Group 2:Button 2"),
                           GroupButton(group_id='2', label="Group 2:Button 3"),
                           ]),
        window=window,
        batch=batch,
        theme=theme)

pyglet.app.run()