from PPlay.window import *
from PPlay.sprite import *
from player import *
from hud import *
import random
import pygame
def hud(power):
    icon = 0

    if power == 'Isur':
        icon = Sprite(assets['hud'] + 'ice.png')
    elif power == 'Firu':
        icon = Sprite(assets['hud'] + 'fire.png')
    elif power == 'Thundur':
        icon = Sprite(assets['hud'] + 'lightning.png')
    else:
        icon =  Sprite(assets['hud'] + 'blank.png')

    return icon

assets = {
    "hud":'assets/hud/',
    "player":'assets/player/',
    "menu":'assets/menu/',
    'tiles':'assets/tiles/',
    'magic':'assets/magic/'
}
config= {
    'controlls':{
        'left':'left',
        'right':'right',
        'up':'up',
        'down':'down',
        'magic':'z',
        'strong_magic':'x',
        'run':'left_shift'
    }
}

# window = Window(864, 576)
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
walking = assets["player"] + 'walking_'
player_animations = [
    walking + 'down-0.6.png',walking + 'up-0.6.png',
    walking + 'left-0.6.png',walking + 'right-0.6.png',
    assets["player"] + 'casting_weak_left-0.6.png',assets["player"] + 'casting_weak_right-0.6.png',
    assets["player"] + 'casting_strong_left-0.6.png',assets["player"] + 'casting_strong_right-0.6.png',
    assets["player"] + 'damage-0.6.png'
    ]
player_animations_names = [
    'walk_d','walk_u',
    'walk_l','walk_r',
    "weak_cast_l","weak_cast_r",
    "strong_cast_l","strong_cast_r",
    "damage_a"
    ]
#Player([Animações],[frames],[durations],[frames_iniciais],[Names]=[])
player = Player(player_animations,[3,3,3,3,4,4,3,3,3],[400,400,400,400,900,900,2000,2000,525],[1,1,1,1,0,0,0,0,0],player_animations_names)
player.x = 486
player.y = 568

player.set_health(3)
player.set_base_health(5)
player.hud.update_values()

player.hud.x = 10
player.hud.y = 10
player.hud.align()

#Variaveis das habilidades
item_ice = True
item_fire = True
item_lightning = True
essence_ice = Sprite(assets['magic'] + 'essenciagelo.png')
essence_fire = Sprite(assets['magic'] + 'essenciafogo.png')
essence_lightning = Sprite(assets['magic'] + 'essenciaraio.png')
essence_ice.x = 300
essence_ice.y = 300
essence_fire.x = 400
essence_fire.y = 400
essence_lightning.x = 500
essence_lightning.y = 500

enemy = Sprite('assets/enemies/Lekro.png')
enemy.x = 400
enemy.y = 300
enemy_center = [enemy.x + enemy.width, enemy.y + enemy.height]

while(True):
    
    player.knockback(window)
    player.cast('',config['controlls'],keyboard,window)

    if player.sprite().collided(enemy):
        player.take_damage(1,enemy_center,120,window)
    
    player.movement(keyboard,window,config['controlls'])    

    ##
    bg.draw()

    for types in tiles:
        for tile in types:
            tile.draw()

    essence_ice.draw()
    if item_fire:
        essence_fire.draw()
    essence_lightning.draw()
    
    enemy.draw()
    player.draw() ## Includes hud.draw()
    ##

    window.update()
