from PPlay.window import *
from PPlay.sprite import *
from player import *
from hud import *
from shards import *
from base_enemy import *
from tile import *
from room import *
from game_map import *
from create_room import *
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

room1 = create_room('room1')
room2 = create_room('room2')
room3 = create_room('room3')
room4 = create_room('room4')
map_of_rooms = [
    [room1,room2,0],
    [room3,room4,0]
    ]
game_map_obj = GameMap(map_of_rooms)

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
player = Player(window,game_map_obj,player_animations,[3,3,3,3,4,4,3,3,3],[400,400,400,400,900,900,2000,2000,525],[1,1,1,1,0,0,0,0,0],player_animations_names)
player.x = 400
player.y = 200

player.set_base_health(10)
player.set_health(10)
player.hud.update_values()

player.hud.x = 10
player.hud.y = 10
player.hud.align()

#Variaveis das habilidades
# essence_fire = Shard(1,300,300)
# essence_ice = Shard(2,400,400)
# essence_lightning = Shard(3,500,200)

# shards_sprites = [essence_fire,essence_ice,essence_lightning]

# enemies = []
# for x in range(4):
#     enemy = BaseEnemy('assets/enemies/Lekro.png')
#     enemy.x = random.randint(30,300)
#     enemy.y = random.randint(100,300)
#     enemies.append(enemy)

# room.enemies = enemies

while(True):
    player.knockback() ## Applying knockback if needed
    player.cast('',config['controlls'],keyboard) ## Casting a spell if needed

    for enemy in player.get_room().enemies: ## Collision with enemies
        if player.sprite().collided(enemy):
            player.take_damage(1,[enemy.x + enemy.width, enemy.y + enemy.height],100)
    
    for shard in player.get_room().shards:
        if shard.collided(player.sprite()):
            player.set_magic(shard.magic)
            shard.remove(shard)
            break
    
    player.movement(keyboard,config['controlls']) ## Movement 

    ##
    # bg.draw()


    game_map_obj.draw(player)
    # room.draw(player,shards_sprites) ## Player,room,enemies
    
    player.draw_hud() ## Hud

    # map_of_rooms[0][0].floors[0][3][4].draw()
    ##
    clock.tick(120) ## Framerate
    window.update()
