class GameMap():
    def __init__(self,rooms):
        self.rooms = rooms
        self.width = len(rooms[0])
        self.height = len(rooms)
    
    def get_room(self,x_y):
        x,y = x_y
        try:
            return self.rooms[y][x]
        except:
            return None
    
    def draw(self,player,dinamic_objects=[]):
        self.get_room(player.room).draw(player,dinamic_objects)
    
    def room_left(self,x_y):
        x,y = x_y
        if x - 1 < 0 or self.get_room([x - 1,y]) == 0:
            return None
        else:
            return [x - 1, y]
    
    def room_right(self,x_y):
        x,y = x_y
        if x + 1 >= self.width:
            return None
        elif self.get_room([x + 1,y]) == 0:
            return None
        else:
            return [x + 1, y]
    
    def room_above(self,x_y):
        x,y = x_y
        if y - 1 < 0 or self.get_room([x, y - 1]) == 0:
            return None
        else:
            return [x, y - 1]
    
    def room_bellow(self,x_y):
        x,y = x_y
        if y + 1 >= self.height:
            return None
        elif self.get_room([x, y + 1]) == 0:
            return None
        else:
            return [x, y + 1]