from PPlay.window import *
from PPlay.sprite import *

assets = {
    "hud":'assets/hud/',
    "player":'assets/player/',
    "menu":'assets/menu/'
}

window = Window(864, 576)
keyboard = window.get_keyboard()
bg = Sprite( assets["menu"] + 'fundo_menu_magnak-0.8.jpg') ## Background diminuido para a janela não ficar muito grande

while(True):
    # bg.draw()
    window.update()