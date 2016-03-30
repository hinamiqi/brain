import pyglet
from Actors import *

backgroundColor = [176, 224, 230, 255]
playerColor = [107, 142, 35]
blockColor = [184, 134, 11]
 
class Window(pyglet.window.Window):
 
	def __init__(self):
		super().__init__(512, 480)
		# pyglet.gl.glColor3f(*rgb_to_pyglet(backgroundColor))
		pyglet.gl.glClearColor(*rgb_to_pyglet(backgroundColor))
		pyglet.clock.schedule_interval(self.update, 1/60)
		self.key_holder = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
		self.player = Player(rgb_to_pyglet(playerColor), 100, 100, 20, 60)
		self.block = Actor(rgb_to_pyglet(blockColor), 200, 200, 100, 100)
		
 
	def on_draw(self):
		self.clear()
		self.player.draw()
		self.block.draw()
 
	def update(self, dt):
		self.player.delta_y = 0
		self.player.delta_x = 0
		self.player.CollisionCheck(self.block)
		if self.key_holder['Up']:
			if self.player.collide['Up'] != True:
				self.player.delta_y = 10
		elif self.key_holder['Down']:
			self.player.delta_y = -10
		elif self.key_holder['Left']:
			self.player.delta_x = -10
		elif self.key_holder['Right']:
			self.player.delta_x = 10
		self.player.Moving()

	def on_key_press(self, key, modifiers):
		if key == pyglet.window.key.UP:
			self.key_holder['Up'] = True
		elif key == pyglet.window.key.DOWN:
			self.key_holder['Down'] = True
		elif key == pyglet.window.key.RIGHT:
			self.key_holder['Right'] = True
		elif key == pyglet.window.key.LEFT:
			self.key_holder['Left'] = True

	def on_key_release(self, key, modifiers):
		if key == pyglet.window.key.UP:
			self.key_holder['Up'] = False
		elif key == pyglet.window.key.DOWN:
			self.key_holder['Down'] = False
		elif key == pyglet.window.key.RIGHT:
			self.key_holder['Right'] = False
		elif key == pyglet.window.key.LEFT:
			self.key_holder['Left'] = False


def rgb_to_pyglet(list):
	result = []
	for i in list:
		result.append(i/255)
	return result


if __name__ == '__main__':
	window = Window()
	pyglet.app.run()