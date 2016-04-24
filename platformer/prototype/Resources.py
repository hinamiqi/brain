#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

# pyglet.resource.path = ["resources/images"]

# pyglet.resource.reindex()

path = "resources/"

tiles = {
            'block': pyglet.image.load(path+"images/ground_grass_2.png"),
            'dblock': pyglet.image.load(path+"images/lava_1.png"),
            'warp': pyglet.image.load(path+"images/warp_1.png")
}

#block = pyglet.resource.image("ground_grass_2.png")

#
path = "resources/"
pyglet.font.add_file(path+"fonts/OptimusPrinceps.ttf")
pyglet.font.load('OptimusPrinceps')