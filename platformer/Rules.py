#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class Game(object):
    
    def __init__(self, player, width, height):
        self.player = player
        self.player_live = True
        self.player_hp = 3
        
        self.victory = False
        # self.x_border = [0, 600]
        # self.y_border = [0, 600]
        self.x_border = [0, width*32]
        self.y_border = [0, height*32]
        print(self.x_border, self.y_border)

    def DeathBlockCollision(self):
        #self.player_live = False
        if self.player.invuln == False:
            self.player_hp -= 1
            self.player.DeathBounce()
            
            if self.player_hp <= 0:
                self.player_live = False
                
            self.player.invuln = True
        
        
    def StageBorder(self, x, y):
        # if (x < self.x_border[0] or x > self.x_border[1]) or \
           # (y < self.y_border[0] or y > self.y_border[1]):
            
            # self.player_live = False
        if y < self.y_border[0]:
            self.player_live = False

