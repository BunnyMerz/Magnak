from PPlay.sprite import *

tile = 'assets/tiles/'
tiles = {
    0:None,
    1:'ground1.png',
    2:'ground2.png',
    3:'ground3.png',
    4:'wall1.png',
    5:'wall2.png',
    6:'wall3.png',
}

class Tile(Sprite):
    def __init__(self,tile_type=0, x=0, y=0, z=0, solid=False, basic_collide=True):
        if tile_type > 3 or tile_type < 7:
            solid=True
        Sprite.__init__(self, tile + tiles[tile_type])
        self.x = x
        self.y = y
        self.z = z