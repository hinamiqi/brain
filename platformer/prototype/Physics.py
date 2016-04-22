#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#max. down_vel
GRAVITY = 10
#0-1
FLYING_MOVESPEED = 0.2
#up_vel max
JUMP_HEIGHT = 14
DEATH_BOUNCE = 10
#0-1
FRICTION = 0.5
INERTION = 1.3

class World(object):
    def __init__(self):
        self.objects = []
        self.grav_const = 10
        self.collide_d = []
        self.collide_u = []
        self.collide_l = []
        self.collide_r = []
        self.warp_collide = False

      
    def collision_check(self, x, y, w, h):
        for block2 in self.objects:
            
            if x < block2.x + block2.width and \
               x + w > block2.x and \
               y < block2.y + block2.height and \
               y + h > block2.y:
                
                if block2.warp == True:
                    self.warp_collide = True
                    return False

                return block2

        return False
 
        
    def touch_check(self, block1):
        for block2 in self.objects:
            #down collide
            if block1.y == (block2.y + block2.height) and \
                (block1.x + block1.width) >= block2.x and \
                block1.x <= (block2.x + block2.width):
                    if not block2 in self.collide_d: 
                        self.collide_d.append(block2)
            else:
                if block2 in self.collide_d:
                    self.collide_d.remove(block2)
            #right collide        
            if block1.x + block1.width == block2.x and \
                 block1.y < block2.y + block2.height and \
                 block1.y + block1.height > block2.y:
                    if not block2 in self.collide_r:
                        self.collide_r.append(block2)
            else:
                if block2 in self.collide_r:
                    self.collide_r.remove(block2)
            #up collide
            if block1.y + block1.height == block2.y and \
                (block1.x + block1.width) >= block2.x and \
                block1.x <= (block2.x + block2.width):
                    if not block2 in self.collide_u: 
                        self.collide_u.append(block2)
            else:
                if block2 in self.collide_u:
                    self.collide_u.remove(block2)
            #left collide        
            if block1.x == block2.x + block2.width and \
                 block1.y < block2.y + block2.height and \
                 block1.y + block1.height > block2.y:
                    if not block2 in self.collide_l:
                        self.collide_l.append(block2)
            else:
                if block2 in self.collide_l:
                    self.collide_l.remove(block2)
            


    def add_object(self, block):
        self.objects.append(block)
