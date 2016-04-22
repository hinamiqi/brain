#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

pyglet.resource.path = ["resources/images"]
pyglet.resource.reindex()

tiles = {
            'block': pyglet.resource.image("ground_grass_2.png"),
            'dblock': pyglet.resource.image("lava_1.png"),
            'warp': pyglet.resource.image("warp_1.png")
}

block = pyglet.resource.image("ground_grass_2.png")
