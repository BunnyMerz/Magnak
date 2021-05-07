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

    @classmethod
    def entity_pixel_colision(cls,body1,body2):
        crop_rect = pygame.Rect((body1.sprite().curr_frame * body1.sprite().width,0),(body1.sprite().width,body1.sprite().height))
        surf1 = pygame.Surface((body1.sprite().width,body1.sprite().height), pygame.SRCALPHA, 32)
        surf1.convert_alpha()
        surf1.blit(body1.sprite().image,crop_rect)
        rect1 = surf1.get_rect()

        crop_rect = pygame.Rect((body2.sprite().curr_frame * body2.sprite().width,0),(body2.sprite().width,body2.sprite().height))
        surf2 = pygame.Surface((body2.sprite().width,body2.sprite().height), pygame.SRCALPHA, 32)
        surf2.convert_alpha()
        surf2.blit(body2.sprite().image,crop_rect)
        rect2 = surf2.get_rect()

        return (UnboundedCollision.perfect_collision(rect1, rect2, surf1, surf2))