from PPlay.sprite import *
import pygame

class Player(Sprite):
    def __init__(self, image_file, frames=1):
        Sprite.__init__(self, image_file, frames)
        self.hp = 20
        self.magic = 0
        self.base_speed = 170
        self.speed = self.base_speed
        self.run = 1.2
    
    def movement(self,keyboard,window):
        moving = False

        if keyboard.key_pressed('right'):
            self.x += self.speed * window.delta_time()
            moving = True
        if keyboard.key_pressed('left'):
            self.x -= self.speed * window.delta_time()
            moving = True
        if keyboard.key_pressed('down'):
            self.update()
            self.y += self.speed * window.delta_time()
            moving = True
        if keyboard.key_pressed('up'):
            self.y -= self.speed * window.delta_time()
            moving = True
        
        if not(moving):
            self.curr_frame = 0
