from tile import *
from room import *
from game_map import *

def create_room(txt_name,x=0,y=0):
    initial_x = x
    initial_y = y
    tile_size = 64
    x = x*tile_size
    y = y*tile_size
    x_off = x
    y_off = y
    room = []
    solids = []
    floor = []
    floor_solids = []
    with open(txt_name+'.txt','r') as map_txt:
        for row in map_txt.readlines():
            if row == '\n':
                room.append(floor)
                solids.append(floor_solids)
                floor = []
                floor_solids = []
                # y += 0.4 * tile_size
                x_off = x
                y_off = y
            else:
                floor_row = []
                x_off = x
                for col in row.strip('\n').split(' '):
                    tile = Tile(col)
                    if tile.solid:
                        floor_solids.append(tile)
                    floor_row.append(tile)
                    tile.x = x_off
                    tile.y = y_off
                    x_off += tile_size
                floor.append(floor_row)
                y_off += tile_size
    if floor != []:
        room.append(floor)
        solids.append(floor_solids)

    return Room(room,solids,[],initial_x,initial_y)