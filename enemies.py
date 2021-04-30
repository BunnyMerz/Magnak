from PPlay.sprite import *
import random
from pit import pitagoras

class BaseEnemy():
    def __init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names=[],x=0,y=0,z=1):
        self.initial_x = x
        self.initial_y = y
        self.initial_z = z
        self.x = x
        self.y = y
        self.z = z
        self.all_animations = []
        self.curr_animation = 0
        self.animations_names = animation_names

        for x in range(len(image_files)):
            sprite = Sprite(image_files[x],frames[x])
            sprite.set_total_duration(total_durations[x])
            sprite.set_initial_frame(initial_frames[x])
            self.all_animations.append(sprite)

        self.invunerable = 0
        self.window = window

        self.base_hp = stats['base_hp']
        self.hp = stats['base_hp']

        self.stun_time = 0
        self.previously_stunned = 0
        self.stun_base_time = self.all_animations[self.name_to_index("damage")].total_duration
        self.knoback_distance = [0,0]
        self.knockback_resistance = 0

        self.room = room

    def take_damage(self,amount,damage_source,distance):
        if self.invunerable > self.window.time_elapsed():
            return

        self.change_health(-amount) ## Vida perdida
        self.stun_time = self.window.time_elapsed() + self.stun_base_time
        self.previously_stunned = 1
        self.set_animation(self.name_to_index("damage"))
        self.sprite().last_time = int(round(time.time() * 1000)) ## Resetar o ciclo da animação
        self.invunerable = self.window.time_elapsed() + 20 ## Invulnerável por um tempo

        try:
            knoback_distance = [(self.x + self.sprite().width/2) - damage_source[0],(self.y + self.sprite().height/2) - damage_source[1]] ## [xi - xo, yi - yo]
            hip = ((knoback_distance[0])**2 + (knoback_distance[1])**2)**(1/2)
            self.knoback_distance = [
                knoback_distance[0] * distance/hip,
                knoback_distance[1] * distance/hip
            ]
        except:
            self.knoback_distance = [0,0]
        
            

    def knockback(self):
        if self.stun_time > self.window.time_elapsed():
            # self.set_animation(8)
            # self.update()
            #//# self.axis = d/t * delta_t                         #//#
            #//# self.axis = pixeis/milesegundo * delta_t segundos #//#
            amount_x = 1000 * self.knoback_distance[0]/self.stun_base_time
            self.move_x(amount_x,1)
            amount_y =  1000 * self.knoback_distance[1]/self.stun_base_time
            self.move_y(amount_y,1)
            self.update_all_animations_coords()
        elif self.previously_stunned == 1:
            self.set_animation(self.name_to_index("base"))
            self.previously_stunned = 0
    
    
    def move_x(self,amount,knockback_movement=0):
        self.change_height()
        if amount > 0:
            past_border = (self.x + self.sprite().width) >= self.window.width
        else:
            past_border = self.x <= 0
        if (self.stun_time > self.window.time_elapsed() and not(knockback_movement)) or past_border:
            return
        for block in self.get_room().get_surrodings(int(self.x/64),int(self.y/64) % self.get_room().width,self.z):
            if self.collision_with_solids(block):
                self.correct_coord(block)
        self.x += amount * self.window.delta_time()
        
    def move_y(self,amount,knockback_movement=0):
        self.change_height()
        if amount > 0:
            past_border = (self.y + self.sprite().height) >= self.window.height
        else:
            past_border = self.y <= 0
        if (self.stun_time > self.window.time_elapsed() and not(knockback_movement))  or past_border:
            return
        for block in self.get_room().get_surrodings(int(self.x/64),int(self.y/64) % self.get_room().width,self.z):
            if self.collision_with_solids(block):
                self.correct_coord(block)
        self.y += amount * self.window.delta_time()
    
    def change_height(self):
        height = [-2,0]
        z_delta = [-1,1]
        for x in range(len(height)):
            stair = self.get_room().get_tile(int(self.x/64),int(self.y/64) % self.get_room().width,self.z + height[x])
            if stair != None:
                if stair.type in ['v','>','<','^']:
                    self.z += z_delta[x]
                    return

    def collision_with_solids(self,solid_block):
        min1_x = self.x
        max1_x = self.x + self.sprite().width
        min1_y = self.y + self.sprite().height * 1/2 
        max1_y = self.y + self.sprite().height

        max2_x = solid_block.x + solid_block.width
        max2_y = solid_block.y + solid_block.height
        if(min1_x >= max2_x or max1_x <= solid_block.x) or (min1_y  >= max2_y or max1_y <= solid_block.y):
            return False
        return True
    
    def correct_coord(self,collided_object): ## Whenever the player collides with something solid, call this function to push him out of the solid block
        side1 = collided_object.x + collided_object.width - self.x 
        side2 = collided_object.x                         - self.sprite().width - self.x
        top1 =  collided_object.y + collided_object.width - self.y - (self.sprite().height * 1/2)
        top2 =  collided_object.y                         - self.y - self.sprite().height

        values = [side2,top1,top2]
        smallest_not_abs = side1
        index = 0

        for x in range(len(values)):
            if abs(values[x]) < abs(smallest_not_abs):
                smallest_not_abs = values[x]
                index = x + 1

        if index == 0 or index == 1:
            self.x += smallest_not_abs
        else:
            self.y += smallest_not_abs

    def change_health(self,delta_amount):
        self.hp += delta_amount
        ## dead?
    
    def update(self):
        sprite = self.all_animations[self.curr_animation]
        sprite.update()
    
    def update_all_animations_coords(self):
        for sprite in self.all_animations:
            sprite.x = self.x
            sprite.y = self.y

    def set_animation(self,index):
        self.curr_animation = index

    def name_to_index(self,name):
        for x in range(len(self.animations_names)):
            if self.animations_names[x].lower() == name.lower():
                return x
    
    def sprite(self):
        return self.all_animations[self.curr_animation]
    
    def draw(self):
        sprite = self.all_animations[self.curr_animation]
        sprite.x,sprite.y = self.x,self.y
        sprite.draw()

    def get_room(self):
        return self.room
    def center(self):
        return [self.x + self.sprite().width/2, self.y + 2*self.sprite().height/3]
    def base(self):
        return [self.x + self.sprite().width/2, self.y + self.sprite().height]

class Lekro(BaseEnemy):
    def __init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names=[],x=0,y=0,z=1):
        BaseEnemy.__init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names,x,y,z)
        self.movement_frequency = 120 ## The higher, the less likely to move. 1 == 100% or 1/x%
        self.jump_distance = {'min':0,'max':100}
        self.vector = [0,0]
        self.next_vector = [0,0]

    def movement(self):
        if self.sprite().curr_frame > 17 or  self.sprite().curr_frame == 0:
            if self.next_vector != None:
                self.vector = self.next_vector
                self.next_vector = None
                self.sprite().curr_frame = 1
            else:
                if random.randint(1,self.movement_frequency) == 1:
                    self.vector = [random.randint(self.jump_distance['min'],self.jump_distance['max']) * (random.randint(0,2) - 1),random.randint(self.jump_distance['min'],self.jump_distance['max']) * (random.randint(0,2) - 1)]
                    if self.vector != [0,0]:
                        self.sprite().curr_frame = 1
                else:
                    self.vector = [0,0]
        elif self.sprite().curr_frame > 2:
            self.move_x(self.vector[0])
            self.move_y(self.vector[1])
        self.knockback()
        if self.sprite().curr_frame != 0:
            self.update()
    
    def death(self):
        pass
    
    def behaviour(self,player):
        distance = pitagoras([self.x,self.y],[player.x,player.y])
        if distance > 300:
            self.movement_frequency = 200
            self.jump_distance = {'min':0,'max':100}
        else:
            self.movement_frequency = 140
            self.jump_distance = {'min':30,'max':200}

            x_axis = (self.x - player.x) * -1
            y_axis = (self.y - player.y) * -1

            if self.jump_distance['max'] < abs(x_axis):
                x_axis = self.jump_distance['max'] * ((x_axis < 0) * -2 + 1)
            if self.jump_distance['max'] < abs(y_axis):
                y_axis = self.jump_distance['max'] * ((y_axis < 0) * -2 + 1)

            self.next_vector = [x_axis, y_axis]