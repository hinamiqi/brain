#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class World(object):
    def __init__(self):
        self.objects = []
        self.grav_const = 10

        
    def CollisionCheck(self, block1):
        for block2 in self.objects:
            if block1.x < block2.x + block2.width and \
               block1.x + block1.width > block2.x and \
               block1.y < block2.y + block2.height and \
               block1.height + block1.y > block2.y:
                
                return block2
        return False
        
    def AddObject(self, block):
        self.objects.append(block)
        print(self.objects)

    def Gravitation(self, vel):
        if vel < self.grav_const:
            vel += 1
        else:
            vel = self.grav_const
        return vel
        # player.move_down(dt)