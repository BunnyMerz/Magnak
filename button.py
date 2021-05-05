import pygame

class Button():
    def __init__(self,image_file,window):
        self.x = 0
        self.y = 0
        self.grey = False
        self.window = window

        self.image = pygame.image.load(image_file).convert_alpha()
        
        rect = self.image.get_rect()
        self.width = rect.width
        self.height = rect.height


        self.bottom = pygame.Surface((self.width,self.height))
        self.bottom.fill((85,85,165))
        self.center = pygame.Surface((self.width - 10,self.height - 10))
        self.center.fill((145,145,213))

    def draw(self):
        self.window.get_screen().blit(self.bottom,(self.x,self.y))
        self.window.get_screen().blit(self.center,(self.x + 5,self.y + 5))

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.grey:
            self.image.set_alpha(100)
            self.window.get_screen().blit(self.image, rect)
            self.image.set_alpha(255)
        else:
            self.window.get_screen().blit(self.image, rect)
    
    def set_position(self,x,y):
        self.x = x
        self.y = y