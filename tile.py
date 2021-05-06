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
    '-':'wall-top.png',
    'tr':'wall-tr.png',
    '.|':'wall-right.png',
    'br':'wall-br.png',
    '_':'wall-bottom.png',
    'L':'wall-bl.png',
    'tl':'wall-tl.png',
    '|.':'wall-left.png',
    "\\":'wall-edge-1.png',
    '/':"wall-edge-2.png",
    'A':'gate1.png',
    'B':'gate2.png',
    'C':'gate3.png',
    'D':'gate4.png',
    'E':'gate.png',
    'S':'solid.png',
    '#':'grid.png',
    "^0":'stairs-up-0.png',
    "^1":'stairs-up-1.png',
    "^2":'stairs-up-2.png',
    'v0':'stairs-down-0.png',
    'v1':'stairs-down-1.png',
    'v2':'stairs-down-2.png',
}

solids = ['4','5','6','-','¬','.|','br','_','L','tp','|.',"\\",'/','S']

class Tile(Sprite):
    def __init__(self,tile_type='0', x=0, y=0, z=0, solid=False, basic_collide=True):
        if tile_type in solids:
            self.solid = True
        else:
            self.solid = False
        if tile_type in ['v','^','<','>']:
            Sprite.__init__(self, tile + tiles[tile_type + str(z)])
        else:
            Sprite.__init__(self, tile + tiles[tile_type])
        self.x = x
        self.y = y
        if tile_type in ['E']:
            self.y -= 64
            self.x -= 64
        self.z = z
        self.type = tile_type