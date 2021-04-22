from PPlay.sprite import *
import pygame

h = 'assets/magic/essencia'
magic_enum = [None,h+'fogo.png',h+'gelo.png',h+'raio.png']

class Shard(Sprite):
    def __init__(self, shard_type, x=0, y=0, z=1):
        Sprite.__init__(self,magic_enum[shard_type])
        self.x = x
        self.y = y
        self.z = z
        self.magic = shard_type
    
    def center(self):
        return [self.x + self.width/2, self.y + 2*self.height/3]
    def base(self):
        return [self.x + self.width/2, self.y + self.height]