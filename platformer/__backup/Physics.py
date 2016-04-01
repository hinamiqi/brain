#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class World(object):
    def __init__(self):
        self.objects = []
    
    def CollisionCheck(self, block1):
        for block2 in self.objects:
            if block1.x < block2.x + block2.width and \
               block1.x + block1.width > block2.x and \
               block1.y < block2.y + block2.height and \
               block1.height + block1.y > block2.y:
                
                self.block = block2
                print('Collision with ', self.block.x, ' ', self.block.y)
                # return True
                
            else:
                # return False
                self.block = False
        return self.block
        # if self.block:
            # return True
        # else:
            # return False
        
    
    # def CollisionDirection(self, block1, block2):
        # if block1.x < block2.x:
        
    def AddObject(self, block):
        self.objects.append(block)
        print(self.objects)
        # self.block = block
    
    # def Interaction(self, player):
        # self.temp = player
        # self.temp.y = self.temp.y + self.temp.up_vel
        # for block in self.objects:
            # if self.CollisionCheck(self.temp, self.block):
                # return self.block.y - player.y + player.height