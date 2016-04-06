#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class World(object):
    def __init__(self):
        self.objects = []
        self.grav_const = 10

      
    def CollisionCheck2(self, x, y, w, h):
        for block2 in self.objects:
            if x < block2.x + block2.width and \
               x + w > block2.x and \
               y < block2.y + block2.height and \
               y + h > block2.y:
                
                #block2.color = [1, 0, 0]
                return block2
            #else:
                #block2.color = [0.61, 0.53, 0.05]
            
        return False
        
    def TouchCheck(self, block1):
        for block2 in self.objects:
            if block1.y == block2.y + block2.height and \
                block1.x < block2.x + block2.width and \
                block1.x + block1.width > block2.x:
                    return True
        
                   
        
    def AddObject(self, block):
        self.objects.append(block)
        #print(self.objects)

    def Gravitation(self, vel):
        if vel < self.grav_const:
            vel += 1
        else:
            vel = self.grav_const
        return vel
        # player.move_down(dt)