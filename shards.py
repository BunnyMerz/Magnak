from PPlay.sprite import *
import pygame

h = 'assets/magic/essencia'
magic_enum = [None,h+'fogo.png',h+'gelo.png',h+'raio.png']

class Shard(Sprite):
    def __init__(self, shard_type, x=0, y=0):
        Sprite.__init__(self,magic_enum[shard_type])
        self.x = x
        self.y = y
        self.magic = shard_type