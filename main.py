from PPlay.window import *
from PPlay.sprite import *
from player import *

assets = {
    "hud":'assets/hud/',
    "player":'assets/player/',
    "menu":'assets/menu/',
    "player":'assets/player/'
}

window = Window(864, 576)
window = Window(972,648)
keyboard = window.get_keyboard()

bg = Sprite( assets["menu"] + 'fundo_menu_magnak-0.9.jpg') 
## Background diminuido para a janela não ficar muito grande

## Setting player up, as well as their animations
player = Player(assets["player"] + 'walking-0.7.png',3)
player.set_total_duration(600)
player.initial_frame = 1


while(True):
    bg.draw()

    player.movement(keyboard,window)

    player.draw()
    window.update()