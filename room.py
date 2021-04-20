from efficient_for import one_time_event

def function_draw(obj):
    obj.draw()

class Room():
    def __init__(self,tiles=[],solids=[],enemies=[]):
        self.tiles = tiles
        self.solids = solids
        self.enemies = enemies
        self.width = len(tiles[0][0])
        self.height = len(tiles[0])
        self.levels = len(tiles)

    
    def draw(self,player,dinamic_objetcs=[]):
        if dinamic_objetcs == [] and self.enemies == []:
            self.simple_draw()
            return
        x_y = player.center()
        indexes = [int(x_y[1]/64 * self.width + x_y[0]/64)]
        for objects in dinamic_objetcs:
            indexes.append(int(objects.y/64 * self.width + objects.x/64))
        for enemy in self.enemies:
            indexes.append(int(enemy.y/64 * self.width + enemy.x/64))

        ids = [x for x in range(len(indexes))]
        objetcs_to_draw = [player] + dinamic_objetcs + self.enemies
        indexes,_,objetcs_to_draw = [ list(tuple) for tuple in zip(*sorted(zip(indexes,ids,objetcs_to_draw))) ]
        print(indexes)
        
        one_time_event(0,self.width * self.height,indexes,objetcs_to_draw,function_draw,self.draw_by_index)
    
    def draw_by_index(self,index):
        self.tiles[0][int(index/self.width)][index % self.width].draw()

    def simple_draw(self):
        for floor in self.tiles:
            for row in floor:
                for tile in row:
                    tile.draw()



        
            