from PPlay.sprite import *
from PPlay.gameimage import *
from math import atan2
from math import degrees
from pit import pitagoras
from pit import pitagoras_class

class LekroSpell():
    def __init__(self,lekros,window):
        self.x = 0
        self.y = 0
        self.sprite_obj = Sprite('assets/magic/thunder.png')
        self.lekros = lekros
        self.window = window

        self.width = 0
        self.height = 0

        self.off_set = 0
        self.surface, _ = self.rotate()

        self.life_span = 10000 + self.window.time_elapsed()

    def sprite(self):
        return self.sprite_obj

    def draw(self):
        if self.life_span < self.window.time_elapsed() or pitagoras_class(self.lekros[0],self.lekros[1]) > 300:
            self.disapear()
            return
        surface,angle = self.rotate()
        self.surface = surface

        x,y = self.lekros[0].x + self.lekros[0].sprite().width/2, self.lekros[0].y + self.lekros[0].sprite().height*3/4

        angle += 180
        if 0 <= angle < 90: 
            y -= self.height
        elif 90 <= angle < 180:
            x -= self.width
            y -= self.height
        elif 180 <= angle < 270:
            x -= self.width

        self.x, self.y = x,y

        self.window.get_screen().blit(surface, (x,y))

    
    def update(self):
        self.sprite().update()

    def rotate(self):
        self.off_set += 2
        delta_x = self.lekros[0].x - self.lekros[1].x

        lekro1_offset = (abs(self.lekros[1].sprite().curr_frame - self.lekros[1].sprite().total_frames/2) * -4) + 40
        lekro1_y = self.lekros[1].y - lekro1_offset

        lekro2_y = self.lekros[0].y

        delta_y = (lekro1_y - lekro2_y)

        angle = degrees(atan2(delta_y, delta_x))
        hip = ((delta_x**2)+(delta_y)**2)**(1/2)

        if hip < 1:
            hip = 1
        if hip > self.sprite().width/2:
            hip = self.sprite().width/2
        if self.off_set > self.sprite().width/2:
            self.off_set = 0

        surface = pygame.Surface((hip,self.sprite().height), pygame.SRCALPHA, 32)
        surface.convert_alpha()
        surface.blit(self.sprite().image,(-self.off_set,0))
        surface = pygame.transform.rotate(surface, angle)

        self.width = surface.get_rect().width
        self.height = surface.get_rect().height

        return surface,angle
    
    def disapear(self):
        for lekro in self.lekros:
            for x in range(len(lekro.attack_sprites)):
                if lekro.attack_sprites[x] == self:
                    lekro.attack_sprites.pop(x)
                    break


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
        self.sprite_class = Sprite('assets/magic/ice_' + direction_name+".png")
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
        self.sprite().x = self.x
        self.sprite().y = self.y
        self.sprite().draw()
    
    def base(self):
        return [self.x + self.sprite().width/2, self.y + self.sprite().height]

    def get_damage(self):
        return self.damage
    
    def sprite(self):
        return self.sprite_class

class StrongIsur():
    def __init__(self,x,y,z):
        self.visual_sprite = Sprite('assets/magic/issur_strong.png',8)
        self.sprite_class = Sprite('assets/magic/issur_strong_hitbox.png',8) ## hitbox
        self.x = x
        self.y = y
        self.z = z
        self.set_position(x,y)
        self.visual_sprite.set_total_duration(1000)
        self.sprite().set_total_duration(1000)
        self.visual_sprite.loop = False
        self.sprite().loop = False
        self.damage = 3
        self.knockback_multiplier = 1

    def draw(self):
        self.visual_sprite.update()
        self.sprite().update()
        self.visual_sprite.draw()
    
    def set_position(self,x,y):
        self.visual_sprite.set_position(x,y)
        self.sprite().set_position(x,y)
        self.x = x
        self.y = y
    
    def base(self):
        return [self.x + self.visual_sprite.width/2, self.y + self.visual_sprite.height]
    
    def get_damage(self):
        return self.damage

    def sprite(self):
        return self.sprite_class

class Liyu():
    def __init__(self,window, direction,x,y,z, damage=1, knockback_multiplier=1):
        self.sprite_class = Sprite('assets/magic/Liyu.png',4)
        self.damage = damage
        self.knockback_multiplier = knockback_multiplier
        self.x = x
        self.y = y
        self.z = z
        self.vector = direction
        self.window = window
        self.speed = 400
        
        self.angle = degrees(atan2(self.vector[1] * -1, self.vector[0]))
        self.sprite().set_total_duration(1400)
        self.sprite().initial_frame = 0
        self.sprite().loop = False
    
    def draw(self):
        self.x += self.vector[0] * self.window.delta_time() * self.speed
        self.y += self.vector[1] * self.window.delta_time() * self.speed

        surface = pygame.Surface((self.sprite().width, self.sprite().height),pygame.SRCALPHA, 32)
        surface.convert_alpha()
        surface.blit(self.sprite().image,(self.sprite().width * self.sprite().curr_frame * -1,0))
        surface = pygame.transform.rotate(surface, self.angle)

        
        self.sprite().x = self.x
        self.sprite().y = self.y
        self.sprite().update()
        self.window.get_screen().blit(surface,(self.x,self.y))
    
    def base(self):
        return [self.x + self.sprite().width/2, self.y + self.sprite().height]
    
    def get_damage(self):
        return self.damage * (self.sprite().curr_frame+1)**(1/2)
    
    def sprite(self):
        return self.sprite_class
