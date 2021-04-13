from PPlay.sprite import *
import pygame

h = 'assets/hud/'
magic_enum = [h+'blank.png',h+'fire.png',h+'ice.png',h+'lightning.png']
hearts = {
    'heart':'assets/hud/heart-0.3.png',
    'blank_heart':'assets/hud/heart_blank-0.3.png'
}


class Hud(): ## Não herda de spirte já que tem varios sprites dentro dele
    def __init__(self,heart_margin=5,hud_margin=10):
        self.x = 0
        self.y = 0

        self.hearts_margin = heart_margin
        self.hud_margin = hud_margin

        self.base_hp = 0
        self.hp = 0
        self.hp_sprites = []
        self.blank_hp_sprites = []

        self.magic = 0
        self.magic_sprite = []
        for magic in magic_enum:
            self.magic_sprite.append(Sprite(magic))
        self.magic_frame_sprite = Sprite('assets/hud/weapon_frame.png')
    

    def draw(self):
        self.magic_sprite[self.magic].draw()
        self.magic_frame_sprite.draw()

        for heart in range(self.hp):
            self.hp_sprites[heart].draw()
        for blank_heart in range(self.base_hp - self.hp):
            self.blank_hp_sprites[self.hp + blank_heart].draw()

    
    def update_values(self):
        delta = self.base_hp - len(self.blank_hp_sprites)
        if delta > 0:
            for _ in range(delta):
                h = Sprite(hearts['heart'])
                bh = Sprite(hearts['blank_heart'])
                self.hp_sprites.append(h)
                self.blank_hp_sprites.append(bh)
        elif delta < 0:
            self.hp_sprites = self.hp_sprites[:delta]
            self.blank_hp_sprites = self.blank_hp_sprites[:delta]
        
        self.align()
    
    def align(self):
        x = self.x
        y = self.y
        self.magic_frame_sprite.x = x
        self.magic_frame_sprite.y = y
        self.magic_sprite[self.magic].x = x
        self.magic_sprite[self.magic].y = y

        hp_x = self.magic_frame_sprite.width + x + self.hud_margin
        for x in range(self.base_hp):
            self.hp_sprites[x].x = hp_x
            self.blank_hp_sprites[x].x = hp_x
            self.hp_sprites[x].y = y
            self.blank_hp_sprites[x].y = y

            hp_x += self.hp_sprites[x].width + self.hearts_margin