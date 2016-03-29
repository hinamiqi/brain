#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import sys
import pymunk
from pyglet.gl import *
from pyglet.window import key
import random

window = pyglet.window.Window(512, 480)

space = pymunk.Space()
space.gravity = (0.0, -700.0)

@window.event
def on_draw():
	window.clear()
	draw_ball(ball)

	
def update(dt):
	space.step(dt)

	
def add_ball(space):
	mass = 1
	radius = 14
	inertia = pymunk.moment_for_circle(mass, 0, radius)
	body = pymunk.Body(mass, inertia)
	x = random.randint(120, 380)
	body.position = x, 500
	verts = [[100, 100], [110, 100], [110, 110], [100, 110]]
	shape = pymunk.Poly(body, verts)
	space.add(body,shape)
	return shape
	

def vert(ball):
		verts = [ball.body.position.x, ball.body.position.y, \
				ball.body.position.x + 10, ball.body.position.y, \
				ball.body.position.x + 10, ball.body.position.y + 10, \
				ball.body.position.x, ball.body.position.y + 10]
		
		return verts
	
def draw_ball(ball):
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
						('v2i', vert(ball)))
	

ball = add_ball(space)
pyglet.clock.schedule_interval(update, 1/50)
pyglet.app.run()