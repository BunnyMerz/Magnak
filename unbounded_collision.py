import pygame
class UnboundedCollision():
    @classmethod
    def perfect_collision(cls, rect1, rect2, surf1, surf2):
        offset_x = (rect2.left - rect1.left)
        offset_y = (rect2.top - rect1.top)
        
        mask_1 = pygame.mask.from_surface(surf1)
        mask_2 = pygame.mask.from_surface(surf2)
        
        if(mask_1.overlap(mask_2, (offset_x, offset_y)) != None):
            return True
        return False

    @classmethod
    def pixel_collision(cls, rect1, rect2, surf1, surf2):
        return (UnboundedCollision.perfect_collision(rect1, rect2, surf1, surf2))