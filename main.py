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
player.x = 400
player.y = 400

weapon_frame = Sprite(assets['hud'] + 'weapon_frame.png')
weapon_frame.x = 10
weapon_frame.y = 10
fire = Sprite(assets['hud'] + 'fire.png')
fire.x = 10
fire.y = 10

hearts = []
hx = 145
hoff = 0
for x in range(9):
    heart = Sprite(assets['hud'] + 'heart-0.3.png')
    heart.x = hx + hoff
    heart.y = 10
    hoff += heart.width + 4
    hearts.append(heart)


while(True):

    player.movement(keyboard,window)

    bg.draw()
    player.draw()
    fire.draw()
    weapon_frame.draw()
    for heart in hearts:
        heart.draw()
    window.update()