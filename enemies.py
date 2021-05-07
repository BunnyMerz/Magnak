from PPlay.sprite import *
import random
from pit import pitagoras
from pit import pitagoras_class
from entity import *
from magic import LekroSpell
from math import atan2
from math import degrees
from math import cos
from math import sin
from shards import *
from heart import *

class BaseEnemy(Entity):
    def __init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names=[], animation_tree=[],x=0,y=0,z=1):
        Entity.__init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names, animation_tree,x,y,z)

class Lekro(BaseEnemy):
    def __init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names=[], animation_tree=[],x=0,y=0,z=1):
        BaseEnemy.__init__(self, window, stats, room, image_files, frames, total_durations, initial_frames, animation_names,animation_tree,x,y,z)
        self.base_hp = 3
        self.hp = 3
        self.movement_frequency = 120 ## The higher, the less likely to move. 1 == 100% or 1/x%
        self.jump_distance = {'min':20,'max':100}
        self.vector = [0,0]
        self.next_vector = [0,0]
        self.attack_sprites = []

    def movement(self):
        self.knockback()
        if self.previously_stunned == 1:
            return
        if self.sprite().curr_frame > self.sprite().final_frame - 4 or self.sprite().curr_frame == 0:
            if self.next_vector != [0,0]:
                self.vector = self.next_vector
                self.next_vector = [0,0]
                self.sprite().curr_frame = 1
            else:
                if random.randint(1,self.movement_frequency) == 1:
                    self.vector = [random.randint(self.jump_distance['min'],self.jump_distance['max']) * (random.randint(0,2) - 1),random.randint(self.jump_distance['min'],self.jump_distance['max']) * (random.randint(0,2) - 1)]
                    if self.vector != [0,0]:
                        self.sprite().curr_frame = 1
                else:
                    self.vector = [0,0]
        elif self.sprite().curr_frame > 5:
            self.move_x(self.vector[0])
            self.move_y(self.vector[1])
        if self.sprite().curr_frame != 0:
            self.update()
    
    def death(self):
        for attack in self.attack_sprites:
            attack.disapear()
        for x in range(len(self.room.enemies)):
            if self.room.enemies[x] == self:
                self.room.enemies.pop(x)
                break
        self.room.shards.append(Shard(3,self.x,self.y,self.z))
        chance_of_heart = random.randint(1,1)
        if chance_of_heart == 1:
            amount = random.randint(1,3)
            self.room.shards.append(Heart(amount,z=self.z,x=self.x,y=self.y))


    def draw(self):
        for attack in self.attack_sprites:
            attack.draw()
        sprite = self.all_animations[self.curr_animation]
        sprite.x,sprite.y = self.x,self.y
        sprite.draw()
    
    def behaviour(self,player):
        distance = pitagoras([self.x,self.y],[player.x,player.y])
        if distance > 300:
            self.movement_frequency = 200
            self.jump_distance = {'min':20,'max':100}
        else:
            self.movement_frequency = 140
            self.jump_distance = {'min':50,'max':200}

            x_axis = (self.x - player.x) * -1
            y_axis = (self.y - player.y) * -1

            if self.jump_distance['max'] < abs(x_axis):
                x_axis = self.jump_distance['max'] * ((x_axis < 0) * -2 + 1)
            if self.jump_distance['max'] < abs(y_axis):
                y_axis = self.jump_distance['max'] * ((y_axis < 0) * -2 + 1)

        
            for enemy in self.room.enemies:
                distance = pitagoras([self.x,self.y],[enemy.x,enemy.y])
                if 0 < distance < 50:
                    alpha_lekros = sin((self.y - enemy.y) / distance)
                    alpha_vector = sin(y_axis / distance)
                    length = x_axis/cos(alpha_vector)
                    x_axis = length * cos(alpha_vector + alpha_lekros)
                    y_axis = length * sin(alpha_vector + alpha_lekros)
                    break

            if self.jump_distance['max'] < abs(x_axis):
                x_axis = self.jump_distance['max'] * ((x_axis < 0) * -2 + 1)
            if self.jump_distance['max'] < abs(y_axis):
                y_axis = self.jump_distance['max'] * ((y_axis < 0) * -2 + 1)

            self.next_vector = [x_axis, y_axis]
    
    def attack(self,list_of_lekros):
        list_of_lekros = list_of_lekros.copy()
        if list_of_lekros == []:
            return
        choice = random.randint(0,len(list_of_lekros) - 1)
        while list_of_lekros[choice].attack_sprites != [] or list_of_lekros[choice] == self or pitagoras_class(self,list_of_lekros[choice]) > 300 or self.z != list_of_lekros[choice].z:
            list_of_lekros.pop(choice)
            if list_of_lekros == []:
                return
            choice = random.randint(0,len(list_of_lekros) - 1)

        attack = LekroSpell([self,list_of_lekros[choice]],self.window)
        self.attack_sprites.append(attack)
        list_of_lekros[choice].attack_sprites.append(attack)