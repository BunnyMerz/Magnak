from PPlay.sprite import *
from PPlay.gameimage import *

class Magic(Sprite):
    def __init__(self,image,damage,knockback_multiplier=1):
        Sprite.__init__()
        self.damage = damage
        self.knockback_multiplier = knockback_multiplier

class LekroSpell(GameImage):
    def __init__(self,x,y,distance,vector):
        GameImage.__init__(self,'assets/magic/thunder.png')
        self.x = x
        self.y = y
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = (x, y)).center)