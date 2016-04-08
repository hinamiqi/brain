#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class Game(object):
    
    def __init__(self):
        self.player_live = True
        self.player_hp = 3
        self.victory = False
        self.x_border = [0, 600]
        self.y_border = [0, 600]
        

    def DeathBlockCollision(self):
        #self.player_live = False
        self.player_hp -= 1
        if self.player_hp <= 0:
            self.player_live = False
        else:
            return True
        
    def StageBorder(self, x, y):
        if (x < self.x_border[0] or x > self.x_border[1]) or \
           (y < self.y_border[0] or y > self.y_border[1]):
            
            self.player_live = False

