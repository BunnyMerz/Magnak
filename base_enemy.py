from PPlay.sprite import *

class BaseEnemy(Sprite):
    def __init__(self,image,frames=1):
        Sprite.__init__(self,image,frames)
        self.z = 1
        
    def center(self):
        return [self.x + self.width/2, self.y + 2*self.height/3]
    def base(self):
        return [self.x + self.width/2, self.y + self.height]