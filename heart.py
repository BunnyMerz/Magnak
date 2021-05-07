from PPlay.sprite import Sprite
import pygame

class Heart(Sprite):
    def __init__(self,amount=1,x=0,y=0,z=1):
        self.z = z
        if amount == 1:
            Sprite.__init__(self,'assets/hud/floor_heart_1.png')
        if amount == 2:
            Sprite.__init__(self,'assets/hud/floor_heart_2.png')
        if amount >= 3:
            Sprite.__init__(self,'assets/hud/floor_heart_3.png')
        self.x = x
        self.y = y
        self.amount = amount

    def base(self):
        return [self.x + self.width/2, self.y + self.height]
    
    def sprite(self):
        return self