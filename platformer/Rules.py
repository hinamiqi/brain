#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class Game(object):
    
    def __init__(self):
        self.player_live = True
        self.victory = False

    def DeathBlockCollision(self):
        self.player_live = False

