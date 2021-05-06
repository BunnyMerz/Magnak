from efficient_for import one_time_event

def function_draw(obj):
    obj.draw()

class Room():
    def __init__(self,floors=[],solids=[],enemies=[],x=0,y=0):
        self.x = x ## Quantos tiles eles está de distância do (0,0).
        self.y = y
        self.floors = floors
        self.enemies = enemies
        self.shards = []

        self.width = len(floors[0][0])
        self.height = len(floors[0])
        self.levels = len(floors)

        self.solids = []
        for floor in solids:
            floor_solids = {}
            for solid in floor:
                floor_solids[int(solid.x/64) + int(solid.y/64) * self.width] = solid
            self.solids.append(floor_solids)

        self.floor_been_drawn = 0
    
    def draw(self,player,dinamic_objetcs=[]):
        
        # <debugging>
        # obj_base = player.base()
        # index = int((obj_base[1]/64 + self.y) * self.width + (obj_base[0]/64 + self.x))
        # print(index, [int(index/self.width),index % self.width])
        # print(player.room,player.z,self.solids)
        # <debugging/>

        all_dinamic_objects = dinamic_objetcs + self.enemies + self.shards
        all_dinamic_objects.append(player) ## Append em player para evitar que o vscode reclame.

        for floor in range(self.levels):
            self.floor_been_drawn = floor
            indexes = []
            dinamic_objects_this_floor,all_dinamic_objects = same_floor(all_dinamic_objects,floor)

            if dinamic_objects_this_floor == []:
                self.simple_draw()
                continue

            for objects in dinamic_objects_this_floor:
                obj_base = objects.base()
                indexes.append(int(int(obj_base[1]/64 + self.y) * self.width + int(obj_base[0]/64 + self.x)))

            ids = [x for x in range(len(indexes))]
            indexes,_,dinamic_objects_this_floor = [ list(tuple) for tuple in zip(*sorted(zip(indexes,ids,dinamic_objects_this_floor))) ]
            
            z = len(indexes) - 1
            b = self.width * self.height
            while(indexes[z] > b and z != 0):
                z -= 1
            z += 1
            indexes,dinamic_objects_this_floor,aside_objs = indexes[:z],dinamic_objects_this_floor[:z],dinamic_objects_this_floor[z:]

            one_time_event(0,self.width * self.height,indexes,dinamic_objects_this_floor,function_draw,self.draw_by_index)
            ## One_time_event(): ## Basicamente faz o seguinte de uma forma eficiente:
            ## z = 0
            ## for x in range(0, self.width * self.height):
            ##      if x in indexes:
            ##          function_draw(objects_to_draw[z])
            ##          z += 1
            ##      else:
            ##          self.draw_by_index(x)

            ## Objs fora do loop de one_time_event()
            for objs in aside_objs:
                objs.draw()

        for leftover_objs in all_dinamic_objects:
            leftover_objs.draw()
    
    def draw_by_index(self,index):
        try:
            tile = self.floors[self.floor_been_drawn][int(index/self.width)][index % self.width]
        except:
            tile = None
        if tile != None:
            tile.draw()

    def simple_draw(self):
        for row in self.floors[self.floor_been_drawn]:
            for c in row:
                c.draw()
    
    def get_tile(self,x,y,z):
        if x < 0 or y < 0 or z < 0:
            return None
        try:
            return self.floors[z][y][x]
        except:
            return None
    
    def get_solids(self,z,indexes):
        solids = []
        for index in indexes:
            try:
                solids.append(self.solids[z][index])
            except:
                pass
                
        return solids
    
    def get_surrodings(self,x,y,z):
        """Returns a 3x3 of tiles of solids in the same z and voids in z-1 unless stairs on z-2 or z"""
        ## Pegar 9 tiles solidos em z
        solid_indexes = []
        vals = [(1,1),(0,1),(1,0),(0,0)]
        for w in range(4):
            for a in range(0,3,2):
                for b in range(0,3,2):
                    solid_indexes.append(((x + (a - 1)* vals[w][0]))+((y +((b-1) * vals[w][1])) * self.width))
        ## Pegar 9 tiles void em z-1
        tiles_under = []
        vals = [(1,1),(0,1),(1,0),(0,0)]
        for w in range(4):
            for a in range(0,3,2):
                for b in range(0,3,2):
                    tile = self.get_tile((x + (a - 1)* vals[w][0]),(y +((b-1) * vals[w][1])),z-1)
                    stairs_below = self.get_tile((x + (a - 1)* vals[w][0]),(y +((b-1) * vals[w][1])),z-2)
                    stairs_above = self.get_tile((x + (a - 1)* vals[w][0]),(y +((b-1) * vals[w][1])),z)
                    if stairs_below != None:
                        if stairs_below.type in ['v','^','>','<']:
                            break
                    if stairs_above != None:
                        if stairs_above.type in ['v','^','>','<']:
                            break
                    if tile != None:
                        if tile.type == '0' or tile.type in ['4','5','6','-','¬','.|','br','_','L','tp','|.',"\\",'/']:
                            tiles_under.append(tile)
                            
        ## Lembrando que o tamanho varia, depenendo de quantos tiles achar
        return self.get_solids(z,solid_indexes) + tiles_under
        #########################################
                
def same_floor(objs,floor):
    new_list = []
    obj = 0
    while(obj < len(objs)):
        if objs[obj].z == floor:
            new_list.append(objs.pop(obj))
        else:
            obj += 1
    return(new_list,objs)



        
            