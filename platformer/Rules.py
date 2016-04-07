#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class Game(object):
    
    def __init__(self):
        self.player_live = True
        self.victory = False
        self.x_border = [0, 512]
        self.y_border = [0, 512]
        

    def DeathBlockCollision(self):
        self.player_live = False
    
    def StageBorder(self, x, y):
        if (x < self.x_border[0] or x > self.x_border[1]) or \
           (y < self.y_border[0] or y > self.y_border[1]):
            
            self.player_live = False

