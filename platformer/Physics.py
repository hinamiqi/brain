#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class World(object):
    # def __init__(self):
        # self.objects = objects
    
    def CollisionCheck(self, block1, block2):
        if block1.x < block2.x + block2.width and \
           block1.x + block1.width > block2.x and \
           block1.y < block2.y + block2.height and \
           block1.height + block1.y > block2.y:
            return True
            
        else:
            return False
    
    # def Direction(self, block1, block2):
        # if block1.x < block2.x:
            
    def AddObject(self, block):
        self.block = block
    
    def Interaction(self, player):
        self.temp = player
        self.temp.y = self.temp.y + self.temp.up_vel
        if self.CollisionCheck(self.temp, self.block):
            return self.block.y
        