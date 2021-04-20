from PPlay.sprite import *
import pygame
from hud import *
import sys

class Player(): ## Não herda de spirte já que tem varios sprites dentro dele
    def __init__(self, image_files, frames, total_durations, initial_frames, animation_names=[]):

        ### Validações
        if len(image_files) > len(frames):
            sys.exit("Missing Player arguments in frames. Expected "+str(len(image_files))+", got "+str(len(frames)))
        if len(image_files) > len(total_durations):
            sys.exit("Missing Player arguments in total_durations. Expected " + str(len(image_files))+", got "+ str(len(total_durations)))
        if len(image_files) > len(initial_frames):
            sys.exit("Missing Player arguments in initial_frames. Expected "+ str(len(image_files)) + ", got",str(len(initial_frames)))
        
        ## Ingame status
        self.base_hp = 20
        self.hp = self.base_hp
        self.magic = 0 ## Magia que ele está usando no momento. Os números ainda precisam ser definidos
        self.base_speed = 170
        self.speed = self.base_speed
        self.run = 0.8 ## porcentagem a acrescentar á velocidade. (base_speed + base_speed * run)

        ## Infos e permissões
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = 0
        self.height = 0
        self.can_move = True
        self.allowed_to_run = True
        self.hide_sprite = False
        ##
        self.casting = 0
        self.cast_cooldown = 500
        self.cast_on_cooldown = 0
        ##
        self.stun = None
        self.knoback_distance = [0,0]
        self.invunerable = 0
        ##
        self.hud = Hud()
        self.hud.base_hp = self.base_hp
        self.hud.hp = self.hp
        self.hud.update_values()

        ## Animações
        self.animations_names = animation_names ## Caso queria usar nome ao invés de index
        self.all_animations = [] ## Sprites
        self.curr_animation = 0 ## Sprites[x]

        for x in range(len(image_files)):
            sprite = Sprite(image_files[x],frames[x])
            sprite.set_total_duration(total_durations[x])
            sprite.set_initial_frame(initial_frames[x])
            self.all_animations.append(sprite)
        ####

    def cast(self,spell,key_settings,keyboard,window):
        if self.stun != None: ## Se estiver Stunado, retorna
            return
        if self.casting > 0: ## 0 significa fazendo nada, se !=, cast tem o valor da animação anterior.
            self.can_move = False
            self.set_animation(self.casting)
            self.update()
            sprite = self.all_animations[self.curr_animation]
            if sprite.get_curr_frame() == sprite.initial_frame:
                self.casting = 0
                self.can_move = True
                self.cast_on_cooldown = window.time_elapsed() + self.cast_cooldown

                orientation = self.index_to_name(self.curr_animation)[-1]
                if orientation == 'l':
                    self.set_animation(2)
                elif orientation == 'r':
                    self.set_animation(3)

        elif self.cast_on_cooldown < window.time_elapsed():
            if keyboard.key_pressed(key_settings['magic']):
                orientation = self.index_to_name(self.curr_animation)[-1]
                if orientation == 'l':
                    self.casting = self.name_to_index("weak_cast_l")
                else:
                    self.casting = self.name_to_index("weak_cast_r")
            elif keyboard.key_pressed(key_settings['strong_magic']):
                orientation = self.index_to_name(self.curr_animation)[-1]
                if orientation == 'r':
                    self.casting = self.name_to_index("strong_cast_r")
                else:
                    self.casting = self.name_to_index("strong_cast_l")

    def take_damage(self,amount,damage_source,distance,window):
        if self.stun != None or self.invunerable > window.time_elapsed():
            return

        self.change_health(-amount) ## Vida perdida

        self.stun = self.index_to_name(self.curr_animation)[-1] ## Orientação quando o dano foi tomado
        self.casting = 0 ## Cancelar qualquer magia

        self.set_animation(8)
        self.all_animations[self.curr_animation].last_time = int(round(time.time() * 1000)) ## Resetar o ciclo da animação
        self.invunerable = window.time_elapsed() + 20 ## Invulnerável por um tempo

        try:
            knoback_distance = [(self.x + self.sprite().width/2) - damage_source[0],(self.y + self.sprite().height/2) - damage_source[1]] ## [xi - xo, yi - yo]
            hip = ((knoback_distance[0])**2 + (knoback_distance[1])**2)**(1/2)
            self.knoback_distance = [
                knoback_distance[0] * distance/hip,
                knoback_distance[1] * distance/hip
            ]
        except:
            self.knoback_distance = [0,0]
        
            

    def knockback(self,window,solid_blocks=[]):
        if self.stun != None:
            self.set_animation(8)
            self.update()
            ## self.axis = d/t * delta_t
            ## self.axis = pixeis/milesegundo * delta_t segundos
            amount_x = self.sprite().total_frames * 1000 * self.knoback_distance[0]/self.sprite().total_duration * window.delta_time()
            self.move_x(amount_x,solid_blocks)
            amount_y = self.sprite().total_frames * 1000 * self.knoback_distance[1]/self.sprite().total_duration * window.delta_time()
            self.move_y(amount_y,solid_blocks)
            self.can_move = False

            if self.sprite().curr_frame == self.sprite().final_frame - 1:
                self.update_all_animations_coords() ## Evitar que alguma spite fique em um local de dano
                self.can_move = True
                self.all_animations[self.curr_animation].curr_frame = 0
                self.set_animation(self.name_to_index("walk_" + self.stun))
                self.stun = None
                self.sprite().unhide()

        

    
    def movement(self,keyboard,window,key_settings,solid_blocks=[]):
        if not(self.can_move):
            return
        moving = False
        allowed_to_run = self.allowed_to_run

        run = keyboard.key_pressed(key_settings["run"])
        if keyboard.key_pressed(key_settings['right']) and not keyboard.key_pressed(key_settings['left']):
            self.move_x((self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time(), solid_blocks)
            moving = True
            self.set_animation(3)
        elif keyboard.key_pressed(key_settings['left']) and not keyboard.key_pressed(key_settings['right']):
            self.move_x( (self.speed + (run * self.run * self.speed * allowed_to_run)) * -window.delta_time(), solid_blocks)
            moving = True
            self.set_animation(2)
        if keyboard.key_pressed(key_settings['down']) and not keyboard.key_pressed(key_settings['up']):
            self.move_y((self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time(), solid_blocks)
            moving = True
            self.set_animation(0)
        elif keyboard.key_pressed(key_settings['up']) and not keyboard.key_pressed(key_settings['down']):
            self.move_y((self.speed + (run * self.run * self.speed * allowed_to_run)) * -window.delta_time(), solid_blocks)
            moving = True
            self.set_animation(1)
        
        if not(moving):
            self.all_animations[self.curr_animation].curr_frame = 0
        else:
            self.update()
        
    def draw(self):
        if self.hide_sprite:
            return
        sprite = self.all_animations[self.curr_animation]
        sprite.x,sprite.y = self.x,self.y
        sprite.draw()
        self.hud.draw()
    
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
    def index_to_name(self,index):
        return self.animations_names[index]


    def set_health(self,new_amount):
        self.hp = new_amount
        self.hud.hp = self.hp

    def change_health(self,delta_amount):
        self.hp += delta_amount
        self.hud.hp = self.hp
    
    def set_base_health(self,new_amount):
        self.base_hp = new_amount
        if self.base_hp < self.hp:
            self.hp = self.base_hp
            self.hud.hp = self.hp
        self.hud.base_hp = self.base_hp
        self.hud.update_values

    def set_magic(self,magic_index):
        self.magic = magic_index
        self.hud.magic = magic_index

    def sprite(self):
        return self.all_animations[self.curr_animation]

    def center(self):
        return [self.x + self.sprite().width, self.y + self.sprite().height]
    
    def move_x(self,amount,solid_blocks=[]):
        for block in solid_blocks:
            if self.collision_with_solids(block):
                self.correct_coord(block)
        self.x += amount
        
    def move_y(self,amount,solid_blocks=[]):
        for block in solid_blocks:
            if self.collision_with_solids(block):
                self.correct_coord(block)
        self.y += amount

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
