#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

# pyglet.resource.path = ["resources/images"]

# pyglet.resource.reindex()

path = "resources/images/"

tiles = {
            'block': pyglet.image.load(path+"ground_grass_2.png"),
            'dblock': pyglet.image.load(path+"lava_1.png"),
            'warp': pyglet.image.load(path+"warp_1.png")
}

#block = pyglet.resource.image("ground_grass_2.png")
