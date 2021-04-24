from PPlay.sprite import *

class Magic(Sprite):
    def __init__(self,image,damage,knockback_multiplier=1):
        Sprite.__init__()
        self.damage = damage
        self.knockback_multiplier = knockback_multiplier