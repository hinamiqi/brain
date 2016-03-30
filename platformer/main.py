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
        self.label = pyglet.text.Label("", font_name='Arial', font_size=20, 
                                           x=10, y=440,
                                           anchor_x='left', anchor_y='bottom')



    def on_draw(self):
        self.clear()
        self.player.draw()
        self.block.draw()
        self.label.draw()

    def update(self, dt):

        self.player.CollisionCheck(self.block)

        #move up:
        if self.key_holder['Up']:
            if self.player.up_vel < self.player.max_speed:
                self.player.up_vel += 1
            else:
                self.player.up_vel = self.player.max_speed

        else:
            if self.player.up_vel > 0:
                self.player.up_vel -= 1
            else:
                self.player.up_vel = 0
        self.player.move_up()

        #move down:
        if self.key_holder['Down']:
            if self.player.down_vel < self.player.max_speed:
                self.player.down_vel += 1
            else:
                self.player.down_vel = self.player.max_speed
        else:
            if self.player.down_vel > 0:
                self.player.down_vel -= 1
            else:
                self.player.down_vel = 0
        self.player.move_down()

        #move right:
        if self.key_holder['Right']:
            if self.player.right_vel < self.player.max_speed:
                self.player.right_vel += 1
            else:
                self.player.right_vel = self.player.max_speed
        else:
            if self.player.right_vel > 0:
                self.player.right_vel -= 1
            else:
                self.player.right_vel = 0
        self.player.move_right()

        #move left:
        if self.key_holder['Left']:
            if self.player.left_vel < self.player.max_speed:
                self.player.left_vel += 1
            else:
                self.player.left_vel = self.player.max_speed
        else:
            if self.player.left_vel > 0:
                self.player.left_vel -= 1
            else:
                self.player.left_vel = 0
        self.player.move_left()

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.UP:
            self.key_holder['Up'] = True
        elif key == pyglet.window.key.DOWN:
            self.key_holder['Down'] = True
        elif key == pyglet.window.key.RIGHT:
            self.key_holder['Right'] = True
        elif key == pyglet.window.key.LEFT:
            self.key_holder['Left'] = True
        elif key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

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