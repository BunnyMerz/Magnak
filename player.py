from PPlay.sprite import *
import pygame
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
        
        ## Infos e permissões
        self.x = 0
        self.y = 0
        self.can_move = True
        self.allowed_to_run = True
        self.casting = 0
        self.cast_cooldown = 500
        self.cast_on_cooldown = 0

        ## Ingame status
        self.hp = 20
        self.magic = 0 ## Magia que ele está usando no momento. Os números ainda precisam ser definidos
        self.base_speed = 170
        self.speed = self.base_speed
        self.run = 0.8 ## porcentagem a acrescentar á velocidade. (base_speed + base_speed * run)

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
        if self.casting > 0:
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
                if orientation == 'l': ## Índice de animação Par é esquerda, impar é direita
                    self.casting = self.name_to_index("weak_cast_l")
                else: #if orientation == 'r':
                    self.casting = self.name_to_index("weak_cast_r")
            elif keyboard.key_pressed(key_settings['strong_magic']):
                orientation = self.index_to_name(self.curr_animation)[-1]
                if orientation == 'r':
                    self.casting = self.name_to_index("strong_cast_r")
                else: #if orientation == 'r':
                    self.casting = self.name_to_index("strong_cast_l")


    
    def movement(self,keyboard,window,key_settings):
        if not(self.can_move):
            return
        moving = False
        allowed_to_run = self.allowed_to_run

        run = keyboard.key_pressed(key_settings["run"])
        if keyboard.key_pressed(key_settings['right']) and not keyboard.key_pressed(key_settings['left']):
            self.x += (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.set_animation(3)
        elif keyboard.key_pressed(key_settings['left']) and not keyboard.key_pressed(key_settings['right']):
            self.x -= (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.set_animation(2)
        if keyboard.key_pressed(key_settings['down']) and not keyboard.key_pressed(key_settings['up']):
            self.y += (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.set_animation(0)
        elif keyboard.key_pressed(key_settings['up']) and not keyboard.key_pressed(key_settings['down']):
            self.y -= (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.set_animation(1)
        
        if not(moving):
            self.all_animations[self.curr_animation].curr_frame = 0
        else:
            self.update()
        
    def draw(self):
        sprite = self.all_animations[self.curr_animation]
        sprite.x,sprite.y = self.x,self.y
        sprite.draw()
    
    def update(self):
        sprite = self.all_animations[self.curr_animation]
        sprite.update()

    def set_animation(self,index):
        self.curr_animation = index
    
    def name_to_index(self,name):
        for x in range(len(self.animations_names)):
            if self.animations_names[x].lower() == name.lower():
                return x
    def index_to_name(self,index):
        return self.animations_names[index]
    