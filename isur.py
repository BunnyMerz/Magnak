from PPlay.sprite import *

directions = {
    'x':{
        0:'',
        1:'r',
        -1:'l'
    },
    'y':{
        0:'',
        -1:'u',
        1:'d'
    }
}

class Isur():
    def __init__(self, window, direction,x,y,z, damage=1, knockback_multiplier=1):
        direction_name = directions['x'][direction[0]] + directions['y'][direction[1]]
        self.sprite = Sprite('assets/magic/ice_' + direction_name+".png")
        self.damage = damage
        self.knockback_multiplier = knockback_multiplier
        self.x = x
        self.y = y
        self.z = z
        self.vector = direction
        self.window = window
        self.speed = 400
    
    def draw(self):
        self.x += self.vector[0] * self.window.delta_time() * self.speed
        self.y += self.vector[1] * self.window.delta_time() * self.speed
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()
    
    def base(self):
        return [self.x + self.sprite.width/2, self.y + self.sprite.height]
        