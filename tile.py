from PPlay.sprite import *

class Tile(Sprite):
    def __init__(self, x=0, y=0, z=0, solid=False):
        Sprite.__init__(self,'assets/tiles/ground.png',3)
        self.x = x
        self.y = y
        self.z = z