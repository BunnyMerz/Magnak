from PPlay.window import *
from PPlay.sprite import *
from player import *
import random

assets = {
    "hud":'assets/hud/',
    "player":'assets/player/',
    "menu":'assets/menu/',
    "player":'assets/player/',
    'tiles':'assets/tiles/'
}
config= {
    'controlls':{
        'left':'left',
        'right':'right',
        'up':'up',
        'down':'down',
        'magic':'z',
        'strong_magic':'x'
    }
}

window = Window(864, 576)
window = Window(972,648)
keyboard = window.get_keyboard()

## Background diminuido para a janela não ficar muito grande
bg = Sprite( assets["menu"] + 'fundo_menu_magnak-0.9.jpg')

ground = Sprite(assets['tiles'] + 'ground.png',3)
amountx = int(window.width/ground.width) + 1
amounty = int(window.height/ground.height) + 1
ground = []
wall = []
gates = []
tiles = [ground,wall,gates]
tilesize = 64
for y in range(amounty):
    for x in range(amountx):
        if x == 6 and y == 0:
            tile = Sprite(assets['tiles'] + 'gate.png',1)
            gates.append(tile)
        elif y == 0 or y == 1: #or y == 0 or x == amountx - 1 or y == amounty - 1:
            tile = Sprite(assets['tiles'] + 'wall.png',3)
            wall.append(tile)
            if random.randint(1,20) == 20:
                tile.curr_frame = 1
        else:
            tile = Sprite(assets['tiles'] + 'ground.png',3)
            ground.append(tile)
            if random.randint(1,10) == 10:
                tile.curr_frame = 1
        tile.x = tilesize * x
        tile.y = tilesize * y

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
    for types in tiles:
        for tile in types:
            tile.draw()
    player.draw()
    fire.draw()
    weapon_frame.draw()
    for heart in hearts:
        heart.draw()
    window.update()