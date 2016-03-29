#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import sys
from pyglet.gl import *
from pyglet.window import key

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]

CollideObjects = []

class Actor(object):
	def __init__(self, color, start_x, start_y, width, height):
		self.color = color
		self.x = start_x
		self.y = start_y
		self.width = width
		self.height = height
		self.speed = 50
		self.vel = 0
		self.msg = ""
	
	def vert(self):
		verts = [self.x, self.y, \
						self.x + self.width, self.y, \
						self.x + self.width, self.y + self.height, \
						self.x, self.y + self.height]
		
		return verts
	
	def draw(self):
		r, g, b = rgb_to_pyglet(self.color)
		glColor3f(r, g, b)
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
						('v2i', self.vert()))
	
	# def move_up(self):
		# if self.msg != 'Top!':
			# self.y += self.speed
	
	# def move_down(self):
		# if self.msg != 'Bot!':
			# self.y -= self.speed
		
	# def move_left(self):
		# if self.msg != 'Left!':
			# self.x -= self.speed
		
	# def move_right(self):
		# if self.msg != 'Right!':
			# self.x += self.speed
			
	def move_up(self):
		if self.msg != 'Top!':
			self.y += self.vel
	
	def move_down(self):
		if self.msg != 'Bot!':
			self.y -= self.vel
		
	def move_left(self):
		if self.msg != 'Left!':
			self.x -= self.vel
		
	def move_right(self):
		if self.msg != 'Right!':
			self.x += self.vel
			
	
	def jump(self):
		if self.msg != 'Top!':
			self.y += self.vel
		
		
	def CollisionCheck(self, block):
		if self.x + self.width == block.x and \
			self.y + self.height > block.y and \
			self.y < block.y + block.height:
			self.msg = "Right!"
			return True
		
		elif self.x == block.x + block.width and \
			self.y + self.height > block.y and \
			self.y < block.y + block.height:
			self.msg = "Left!"
			return True
			
		elif self.y + self.height == block.y and \
			self.x + self.width > block.x and \
			self.x < block.x + block.width:
			self.msg = "Top!"
			return True
			
		elif self.y == block.y + block.height and \
			self.x + self.width > block.x and \
			self.x < block.x + block.width:
			self.msg = "Bot!"
			return True
		else:
			self.msg = ""
	
	
	def update(self, dt):

		if self.vel > 0:
			print(self.vel)
			self.vel -= 1
		elif self.vel < 0:
			self.vel = 0
		
		for key in keys_held:
			if key == pyglet.window.key.UP:
				self.vel = self.speed
				self.move_up()
			elif key == pyglet.window.key.DOWN:
				self.vel = self.speed
				self.move_down()
			elif key == pyglet.window.key.RIGHT:
				self.vel = self.speed
				self.move_right()
			elif key == pyglet.window.key.LEFT:
				self.vel = self.speed
				self.move_left()
			elif key == pyglet.window.key.SPACE:
				self.vel = self.speed * 2
				self.jump()
	

def rgb_to_pyglet(list):
	result = []
	for i in list:
		result.append(i/255)
	return result[0], result[1], result[2]
	
def clr_format(value):
	return value/255

window = pyglet.window.Window(512, 480)
r, g, b = rgb_to_pyglet(backgroundColor)
pyglet.gl.glClearColor(r, g, b, 1)
player = Actor(playerColor, 50, 50, 10, 30)
block = Actor(blockColor, 200, 200, 100, 100)
CollideObjects.append(block)
keys_held = []
label = pyglet.text.Label("",
                          font_name='Arial',
                          font_size=20, x=10, y=440,
                          anchor_x='left', anchor_y='bottom')
						  


@window.event
def on_draw():
	window.clear()
	# r, g, b = rgb_to_pyglet(playerColor)
	# glColor3f(r, g, b)
	# #verts = [10, 10, 10, 100, 100, 100, 100, 10]
	# verts = player.update()
	# pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, \
						# ('v2i', verts))
	player.draw()
	block.draw()
	if player.CollisionCheck(block):
		label.text = player.msg
		label.draw()
	
	

@window.event
def on_key_press(key, modifiers):
	keys_held.append(key)

	# if key == pyglet.window.key.UP:
		# player.move_up()
	# elif key == pyglet.window.key.DOWN:
		# player.move_down()
	# elif key == pyglet.window.key.RIGHT:
		# player.move_right()
	# elif key == pyglet.window.key.LEFT:
		# player.move_left()

@window.event
def on_key_release(key, modifiers):
	keys_held.pop(keys_held.index(key))
	

	# for key in keys_held:
		# if key == pyglet.window.key.UP:
			# player.move_up()
		# elif key == pyglet.window.key.DOWN:
			# player.move_down()
		# elif key == pyglet.window.key.RIGHT:
			# player.move_right()
		# elif key == pyglet.window.key.LEFT:
			# player.move_left()
		# elif key == pyglet.window.key.SPACE:
			# vel = 10
	

pyglet.clock.schedule_interval(player.update, 1/60)
pyglet.app.run()