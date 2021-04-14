from PPlay.sprite import *

class Magic(Sprite):
    def __init__(self,damage,knockback_multiplier=1):
        self.damage = damage
        self.knockback_multiplier = knockback_multiplier