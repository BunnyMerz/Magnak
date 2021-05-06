import sys
import pygame
from button import *

class Menu():
    def __init__(self, bg, options, window, side_space=5, line_space=10, x=0, y=0):
        self.x = x
        self.y = y
        self.bg = bg
        self.options = {}
        self.option_index = [0]
        self.difficulty = 1
        self.window = window

        self.width = []
        self.line_space = line_space
        self.side_space = side_space

        for index in options: ## Botões um em cima do outro, a partir do fundo; Independe de quantidade
            widest = 0
            if index == (0,0):
                initial_x = x
                initial_y = y
            else:
                initial_x = x - self.get_width(index[1])
                initial_y = self.get_page(index[1] - 1)[index[0]].y
            offset = 0
            self.options[index] = []
            for path in options[index]:
                button = Button(path,self.window)
                button.set_position(initial_x - button.width, initial_y + offset)
                offset += button.height + line_space
                self.options[index].append(button)
                if button.width > widest:
                    widest = button.width
            self.width.append(widest)

    def draw(self):
        mouse = self.window.get_mouse()
        holding_left_mouse = False ## Evitar que o mouse clique em várias opts
        while(True):
            self.window.get_screen().blit(self.bg, (0,0))

            for index in self.option_index:
                page = self.get_page(index)
                for x in range(len(page)):
                    page[x].draw()

            z = -1
            for index in self.option_index:
                z += 1
                page = self.get_page(index)
                for x in range(len(page)):
                    if mouse.is_over_object(page[x]):
                        if not page[x].grey:
                            self.hover(page[x],self.width[z])
                            if mouse.is_button_pressed(1) and not(holding_left_mouse):
                                if self.change_index(index,x) == 'new_game':
                                    return 'Game'
                                elif self.change_index(index,x) == 'contiune':
                                    return 'Game'
                                holding_left_mouse = True
                                break ## Evitar que o for continue em cima de uma lista nova, já que change_index() mudará
                            elif not(mouse.is_button_pressed(1)):
                                holding_left_mouse = False
                else:
                    continue
                break ## Break de for duplo, só chega aqui caso o primeiro Break seja chamado


            self.window.update()
    
    def change_index(self,y,x):
        self.option_index = self.option_index[:y+1]
        self.open_page(x,y)
        button = [x,y] ## Mapping do que os butões fazem, dependem de como o dic de opts está
        # button = qual página, qual botão dessa página
        # [Qual opção, qual página], opção começa de 0, página de 1
        # {(0,0):[]} onde (x,y) se refere á algum outro botão e [] são os botões daquela página
        if button == [0,0]: ## Continue
            return 'continue'

        if button == [1,0]: ## New Game
            return 'new_game'
        
        if button == [3,0]: ## Leave
            sys.exit(1)

    def get_width(self,index):
        x = 0
        while(index != 0):
            x += 1
            index = list(self.options.keys())[index - 1][1]

        total_width = 0
        for z in range(x):
            total_width += self.width[z]
        total_width += self.side_space * (x)
        return total_width
        
    def get_page(self,x):
        z = 0
        for pages in self.options:
            if z == x:
                return self.options[pages]
            z += 1
        
    def search_page(self,x,y):
        z = 0
        for coord in self.options:
            if coord == (x,y+1):
                return z
            z += 1
    
    def open_page(self,x,y):
        page = self.search_page(x,y)
        if page != None:
            self.option_index.append(page)
    
    def hover(self,button,width):
        padding_left = self.side_space * 0.6
        height = button.height
        surface = pygame.Surface((width + padding_left,height))
        surface.fill((210,210,75))
        surface.set_alpha(120)
        x = button.x - width + button.width - padding_left
        y = button.y
        self.window.get_screen().blit(surface,(x,y))

        