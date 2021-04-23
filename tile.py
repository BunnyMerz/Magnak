from PPlay.sprite import *

tile = 'assets/tiles/'
tiles = {
    '0':'empty.png',
    '1':'ground1.png',
    '2':'ground2.png',
    '3':'ground3.png',
    '4':'wall1.png',
    '5':'wall2.png',
    '6':'wall3.png',
    'A':'gate1.png',
    'B':'gate2.png',
    'C':'gate3.png',
    'D':'gate4.png',
}

solids = ['4','5','6']

class Tile(Sprite):
    def __init__(self,tile_type='0', x=0, y=0, z=0, solid=False, basic_collide=True):
        if tile_type in solids:
            self.solid = True
        else:
            self.solid = False
        Sprite.__init__(self, tile + tiles[tile_type])
        self.x = x
        self.y = y
        self.z = z
        self.type = tile_type