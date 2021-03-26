from PPlay.sprite import *
import pygame
import sys

class Player():
    def __init__(self, image_files, frames, total_durations, initial_frames):
        if len(image_files) > len(frames):
            sys.exit("Missing Player arguments in frames. Expected "+str(len(image_files))+", got "+str(len(frames)))
        if len(image_files) > len(total_durations):
            sys.exit("Missing Player arguments in total_durations. Expected " + str(len(image_files))+", got "+ str(len(total_durations)))
        if len(image_files) > len(initial_frames):
            sys.exit("Missing Player arguments in initial_frames. Expected "+ str(len(image_files)) + ", got",str(len(initial_frames)))
        self.x = 0
        self.y = 0

        self.hp = 20
        self.magic = 0
        self.base_speed = 170
        self.speed = self.base_speed
        self.run = 0.3


        self.all_animations = []
        self.curr_animation = 0

        print(self.all_animations)
        for x in range(len(image_files)):
            sprite = Sprite(image_files[x],frames[x])
            sprite.set_total_duration(total_durations[x])
            sprite.set_initial_frame(initial_frames[x])
            self.all_animations.append(sprite)
        print(self.all_animations)

    
    def movement(self,keyboard,window,allowed_to_run=True):
        moving = False

        run = keyboard.key_pressed("left_shift")
        if keyboard.key_pressed('right') and not keyboard.key_pressed('left'):
            self.x += (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.curr_animation = 3
        elif keyboard.key_pressed('left') and not keyboard.key_pressed('right'):
            self.x -= (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.curr_animation = 2
        if keyboard.key_pressed('down') and not keyboard.key_pressed('up'):
            self.y += (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.curr_animation = 0
        elif keyboard.key_pressed('up') and not keyboard.key_pressed('down'):
            self.y -= (self.speed + (run * self.run * self.speed * allowed_to_run)) * window.delta_time()
            moving = True
            self.curr_animation = 1
        
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