#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet

class Actor(object):

	def __init__(self, color, start_x, start_y, width, height):
		self.color = color
		self.x = start_x
		self.y = start_y
		self.width = width
		self.height = height
		self.speed = 50
		self.vel = 0
		self.collide = {'Up': False, 'Down': False, 'Left': False, 'Right': False}

	def vert(self):
		verts = [self.x, self.y,
				 self.x + self.width, self.y,
				 self.x + self.width, self.y + self.height,
				 self.x, self.y + self.height]
		return verts

	def draw(self):
#		 r, g, b = self.rgb_to_pyglet(self.color)
		pyglet.gl.glColor3f(*self.color)
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
						('v2i', self.vert()))

class Player(Actor):
	def __init__(self, color, start_x, start_y, width, height):
		super().__init__(color, start_x, start_y, width, height)
		self.delta_x = 0
		self.delta_y = 0

	def CollisionCheck(self, block):
		if self.x + self.width == block.x and \
			self.y + self.height > block.y and \
			self.y < block.y + block.height:
			self.collide['Up'] = True


		elif self.x == block.x + block.width and \
			self.y + self.height > block.y and \
			self.y < block.y + block.height:
			self.collide['Left'] = True


		elif self.y + self.height == block.y and \
			self.x + self.width > block.x and \
			self.x < block.x + block.width:
			self.collide['Top!'] = True


		elif self.y == block.y + block.height and \
			self.x + self.width > block.x and \
			self.x < block.x + block.width:
			self.collide['Bot'] = True

		else:
			self.collide = {'Up': False, 'Down': False, 'Left': False, 'Right': False}

	def Moving(self):
		
		if self.delta_x != 0:
			self.x = self.x + self.delta_x
		if self.delta_y != 0:
			self.y = self.y + self.delta_y























