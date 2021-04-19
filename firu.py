from PPlay.sprite import *
from magic import Magic

class Firu(Magic):
    def __init__(self,damage,knockback_multiplier=1):
        Magic.__init__(self,damage,knockback_multiplier)
        