from PPlay.window import *
from PPlay.sprite import *
from player import *
from hud import *
from shards import *
from base_enemy import *
from tile import *
from room import *
import random
import pygame

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
clock = pygame.time.Clock()

## Background diminuido para a janela não ficar muito grande
bg = Sprite( assets["menu"] + 'fundo_menu_magnak-0.9.jpg')

# ground = []
# wall = []
# gates = []
# tiles = [ground,wall,gates]
tilesize = 64
amountx = int(window.width/tilesize) + 1
amounty = int(window.height/tilesize) + 1
room_tiles = []
for y in range(amounty + 2):
    row = []
    for x in range(amountx):
        if y == 7:
            tile = (Tile(None))
            row.append(tile)
        else:
            tile = Tile(1)
            row.append(tile)
        tile.x = tilesize * x
        tile.y = tilesize * y
    room_tiles.append(row)

tilesize = 64
solid_tiles = []
room_tiles2 = []
for y in range(amounty + 2):
    row = []
    for x in range(amountx):
        if x == 6 and y == 0:
            tile = Tile('gate1')
            row.append(tile)
        elif x == 7 and y == 0:
            tile = Tile('gate2')
            row.append(tile)
        elif x == 6 and y == 1:
            tile = Tile('gate3')
            row.append(tile)
        elif x == 7 and y == 1:
            tile = Tile('gate4')
            row.append(tile)
        elif x == 5 and y == 5:
            tile = Tile(6)
            row.append(tile)
            solid_tiles.append(tile)
        elif (y == 0 or y == 1):
            tile = Tile(5)
            row.append(tile)
            solid_tiles.append(tile)
        else:
            row.append(Tile(None))
        tile.x = tilesize * x
        tile.y = tilesize * y
    room_tiles2.append(row)

room = Room([room_tiles,room_tiles2],[[],solid_tiles])

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
player.x = 300
player.y = 400

player.set_base_health(10)
player.set_health(10)
player.hud.update_values()

player.hud.x = 10
player.hud.y = 10
player.hud.align()

#Variaveis das habilidades
essence_fire = Shard(1,300,300)
essence_ice = Shard(2,400,400)
essence_lightning = Shard(3,500,500)

shards_sprites = [essence_fire,essence_ice,essence_lightning]

enemies = []
for x in range(4):
    enemy = BaseEnemy('assets/enemies/Lekro.png')
    enemy.x = random.randint(30,300)
    enemy.y = random.randint(100,300)
    enemies.append(enemy)

room.enemies = enemies

player.room = room
while(True):
    player.knockback(window) ## Applying knockback if needed
    player.cast('',config['controlls'],keyboard,window) ## Casting a spell if needed

    for enemy in room.enemies: ## Collision with enemies
        if player.sprite().collided(enemy):
            player.take_damage(1,[enemy.x + enemy.width, enemy.y + enemy.height],100,window)
    
    for shard in shards_sprites:
        if shard.collided(player.sprite()):
            player.set_magic(shard.magic)
            shards_sprites.remove(shard)
            break
    
    player.movement(keyboard,window,config['controlls']) ## Movement 

    ##
    bg.draw()

    room.draw(player,shards_sprites) ## Player,room,enemies
    
    player.draw_hud() ## Hud

    ##
    clock.tick(120) ## Framerate
    window.update()
